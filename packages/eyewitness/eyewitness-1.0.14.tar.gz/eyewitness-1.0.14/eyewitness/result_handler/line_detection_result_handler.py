import arrow
from linebot import LineBotApi
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction
)
from eyewitness.config import BBOX, LINE_FALSE_ALERT_MSG_TEMPLATE, LINE_PLATFROM
from eyewitness.detection_utils import DetectionResultHandler
from eyewitness.models.feedback_models import RegisteredAudience
from eyewitness.models.db_proxy import DATABASE_PROXY


class LineAnnotationSender(DetectionResultHandler):
    def __init__(self, channel_access_token, image_url_handler, raw_image_url_handler=None,
                 audience_ids=None, update_audience_period=0, detection_result_filter=None,
                 detection_method=BBOX, database=None):
        """
        Parameters
        ----------
        audience_ids: set
            line audience ids
        channel_access_token: str
            channel_access_token
        image_url_handler: Callable
            compose drawn image to image_url
        update_audience_period: int
            the period(seconds) that update the audience_ids from audience model, 0 will not update
        detection_result_filter: Callable
            a function check if the detection result to sent or not
        detection_method: str
            detection method
        database: peewee.Database
            peewee database obj, used to query registered audiences
        """
        self.water_mark_time = arrow.now()
        self.update_audience_period = update_audience_period
        self.line_bot_api = LineBotApi(channel_access_token)
        self.detection_result_filter = detection_result_filter
        self._detection_method = detection_method
        self.database = database
        self.create_db_table()
        if audience_ids is None:
            self.audience_ids = self.get_registered_audiences()
        else:
            self.audience_ids = audience_ids

        # setup image_url handler and raw_image_url_handler
        self.image_url_handler = image_url_handler
        if raw_image_url_handler is not None:
            self.raw_image_url_handler = raw_image_url_handler
        else:
            self.raw_image_url_handler = self.image_url_handler

    @property
    def detection_method(self):
        """str: detection_method"""
        return self._detection_method

    def create_db_table(self):
        """create the RegisteredAudience if not exist
        """
        self.check_proxy_db()
        RegisteredAudience.create_table()

    def get_registered_audiences(self):
        """ get the RegisteredAudience id list
        """
        if self.database is None:
            raise("the database is not set")
        self.check_proxy_db()
        query = RegisteredAudience.select().where(RegisteredAudience.platform_id == LINE_PLATFROM)
        audiences = set(i.user_id for i in query)
        return audiences

    def check_proxy_db(self):
        """check if the db proxy is correct one, if not initialize again.
        """
        if not (self.database is DATABASE_PROXY.obj):
            DATABASE_PROXY.initialize(self.database)

    def audience_update(self):
        """
        update the audiences from RegisteredAudience model
        """
        if self.update_audience_period and self.database is not None:
            diff_seconds = (arrow.now() - self.water_mark_time).total_seconds()
            if diff_seconds > self.update_audience_period:
                audience_ids = self.get_registered_audiences()
                self.audience_ids = audience_ids

    def _handle(self, detection_result):
        # update audience
        self.audience_update()

        # check if detection result need to sent_out
        if self.detection_result_filter(detection_result):
            image_url = self.image_url_handler(detection_result.drawn_image_path)
            # TODO: consider a better way to generate raw_image_url
            raw_image_url = self.raw_image_url_handler(detection_result.drawn_image_path)
            false_alert_feedback_text = LINE_FALSE_ALERT_MSG_TEMPLATE.format(
                image_id=str(detection_result.image_id), meta='')
            self.send_annotation_button_msg(image_url, raw_image_url, false_alert_feedback_text)

    def send_annotation_button_msg(self, image_url, raw_image_url, false_alert_feedback_text):
        """
        sent line botton msg to audience_ids

        Parameters
        ----------
        image_url: str
            the url of image

        raw_image_url: str
            the url of raw_image, which might be another bigger/clear image

        false_alert_feedback_text: str
            false_alert msg used to sent to feedback_handler
        """
        buttons_msg = TemplateSendMessage(
            alt_text='object detected',
            template=ButtonsTemplate(
                thumbnail_image_url=image_url,
                title='object detected',
                text='help to report result',
                actions=[
                    MessageAction(
                        label='Report Error (錯誤回報)',
                        text=false_alert_feedback_text
                    ),
                    URIAction(
                        label='full image (完整圖片)',
                        uri=raw_image_url
                    )
                ]
            )
        )
        if self.audience_ids:  # check if audiences
            self.line_bot_api.multicast(list(self.audience_ids), buttons_msg)
