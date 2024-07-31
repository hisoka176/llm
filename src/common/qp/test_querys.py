from unittest import TestCase

from src.common.qp.querys import ExtraTableName


class TestExtraTableName(TestCase):

    def test_content(self):
        extra = ExtraTableName()
        test = ['表gdm_02_pv_basic_di的留存',
                'gdm_02_outweb_basic_di的生成fds',
                'adm_04_app_rcmd_user_biztype_di',
                'gdm_04_resource_first_recommend_da',
                'gdm_04_3gc_info_video_play_detail_di',
                'gdm_02_app_owner_active_di']
        for t in test:
            print(extra.extract(t))
