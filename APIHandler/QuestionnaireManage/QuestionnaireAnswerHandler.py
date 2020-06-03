from BaseHandler import xsrf, authenticated
from QuestionnaireBaseHandler import QuestionnaireBaseHandler
from orm import AnswerOptionTable, QuestionNaireQuestionTable, QuestionNaireOptionTable
from typing import List, Text
import csv
import os


class QuestionnaireSubmitHandler(QuestionnaireBaseHandler):
    def initialize(self):
        super(QuestionnaireSubmitHandler, self).initialize()
        self.PARSING_FAILED = 1
        self.QUESTIONNAIRE_NOT_FOUND = 2

    @xsrf
    async def post(self, *arg, **kwargs):
        # 问卷提交
        # 1. 解析数据
        # 2. 验证问卷是发布状态
        # 3. 记录选项/填空项
        # todo 日志管理 此模块失败需要记录日志
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self)
        q_id = json_data.get('Q_ID')
        if not await self.is_questionnaire_published(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not await self.save_answer(json_data):
            return self.raise_HTTP_error(403, self.PARSING_FAILED)

    async def save_answer(self, json_data: dict) -> bool:
        # 记录选项，参考数据库设计
        engine = self.get_engine()
        q_id = json_data.get('q_id')
        content = json_data.get('content')
        if not content:
            return False
        try:
            # 创建事务
            async with engine.acquire() as conn:
                for question in content:
                    question_id = question.get('question_id')
                    question_type = int(question.get('question_type'))
                    options: List[int] = question.get(
                        'option') if question_type == 0 or question_type == 1 else None
                    option_content = question.get('content') if question_type == 2 else None
                    if not (options or option_content):
                        return False
                    if options:
                        for option_id in options:
                            await conn.execute(AnswerOptionTable.insert().values(
                                QO_ID=option_id,
                                QQ_ID=question_id,
                                QI_ID=q_id,
                                QO_Type=question_type,
                                AO_Content=option_content
                            ))
                    else:
                        await conn.execute(AnswerOptionTable.insert().values(
                            QO_ID=1,
                            QQ_ID=question_id,
                            QI_ID=q_id,
                            QO_Type=question_type,
                            AO_Content=option_content
                        ))
                # 一并提交
                await conn._commit_impl()
        except:
            return False
        return True


class QuestionnaireResultHandler(QuestionnaireBaseHandler):
    def initialize(self):
        super(QuestionnaireResultHandler, self).initialize()
        self.question_map = {}
        self.option_map = {}

    async def get_question_content(self, qi_id, qq_id) -> Text:
        content = self.question_map.get(str(qq_id))
        if not content:
            engine = self.get_engine()
            async with engine.acquire() as conn:
                result = await conn.execute(QuestionNaireQuestionTable.select()
                                            .where(QuestionNaireQuestionTable.c.QQ_ID == qq_id)
                                            .where(QuestionNaireQuestionTable.c.QI_ID == qi_id)
                                            )
                question_info = await result.fetchone()[0]
            content = question_info.content
            self.question_map[str(qq_id)] = content
        return content

    async def get_option_content(self, qi_id, qq_id, qo_id) -> Text:
        content = self.option_map.get(str(qq_id) + ':' + str(qo_id))
        if not content:
            engine = self.get_engine()
            async with engine.acquire() as conn:
                result = await conn.execute(QuestionNaireOptionTable.select()
                                            .where(QuestionNaireOptionTable.c.QO_ID == qo_id)
                                            .where(QuestionNaireOptionTable.c.QI_ID == qi_id)
                                            .where(QuestionNaireOptionTable.c.QQ_ID == qq_id)
                                            )
                question_info = await result.fetchone()[0]
            content = question_info.content
            self.option_map[str(qq_id) + ':' + str(qo_id)] = content
        return content

    @xsrf
    @authenticated
    async def get(self, *args, **kwargs):
        # 问卷结果全量导出，仅接受查询停用的问卷
        # 1. 用户鉴权
        # 2. 问卷状态检查
        # 3. 查找是否有csv缓存，若无，则将查询结果写入csv，返回文件名
        # 4. 提供csv下载服务
        try:
            q_id = int(self.get_query_argument('Q_ID'))
        except:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not await self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not await self.is_questionnaire_inactivate(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        filename = await self.get_all_result(q_id)
        self.set_header("Content-Type", "text/csv")
        self.set_header('Content-Disposition', 'attachment; filename=' + 'Result')
        with open(filename, 'rb') as f:
            while True:
                data = f.read(2048)
                if not data:
                    break
                self.write(data)
        self.finish()

    async def get_all_result(self, q_id) -> Text:
        # 将问卷结果写入缓存文件，返回文件名
        # todo 缓存文件定期清理
        engine = self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(AnswerOptionTable.select()
                                        .where(AnswerOptionTable.c.QI_ID == q_id))
            options = await result.fetchall()

        csv_headers = ['题号', '题目', '选项号', '选项', '选择/回答']
        file_name = './Temp/' + str(q_id) + '.csv'
        if os.path.exists(file_name):
            return file_name
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, csv_headers)
            for option in options:
                question_id = option.QQ_ID
                question_content = await self.get_question_content(q_id, question_id)
                option_id = option.QO_ID
                option_content = await self.get_option_content(q_id, question_id, option)
                question_type = option.QO_Type
                content = '是' if question_type == 0 or question_type == 1 else option.AO_Content
                writer.writerow({
                    '题号': question_id,
                    '题目': question_content,
                    '选项号': option_id,
                    '选项': option_content,
                    '选择/回答': content,
                })
        return file_name


class QuestionnaireStatisticsHandler(QuestionnaireBaseHandler):
    @xsrf
    @authenticated
    async def get(self, *args, **kwargs):
        # todo 问卷结果统计
        pass


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSubmit/", QuestionnaireSubmitHandler),
    (r"/api/v1/questionnaireResultGet/", QuestionnaireResultHandler),
    (r"/api/v1/questionnaireStatistics/", QuestionnaireStatisticsHandler)
]
