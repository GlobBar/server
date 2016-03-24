from places.models import Place


class PlaceRepository():

    def getMonthReports(self, parameters):
        tz_delta = parameters['tz_delta']
        str_pk = parameters['str_pk']
        correct_limit_from = parameters['correct_limit_from']
        correct_limit_count = parameters['correct_limit_count']
        pk = parameters['pk']
        frt = parameters['frt']


        simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*30) HOUR, %s) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt)
            )
        return simple_reports

    def getMonthReportsHot(self, parameters):
        tz_delta = parameters['tz_delta']
        pk = parameters['pk']
        frt = parameters['frt']

        hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*30) HOUR, %s) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk,  frt)
            )
        return hot_reports

    # WEEK
    def getWeekReportsHot(self, parameters):
        tz_delta = parameters['tz_delta']
        pk = parameters['pk']
        frt = parameters['frt']

        hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND (CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*7) HOUR, %s)) '
                'AND (CONVERT_TZ(report_report.created,\'+00:04\', \''+tz_delta+'\') < DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*6) HOUR, %s)) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk, frt, frt)
            )
        return hot_reports

    def getWeekReports(self, parameters):
        tz_delta = parameters['tz_delta']
        str_pk = parameters['str_pk']
        correct_limit_from = parameters['correct_limit_from']
        correct_limit_count = parameters['correct_limit_count']
        pk = parameters['pk']
        frt = parameters['frt']

        simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND (CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*7) HOUR, %s)) '
                 'AND (CONVERT_TZ(report_report.created,\'+00:04\', \''+tz_delta+'\') < DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*6) HOUR, %s)) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt, frt)
            )
        return simple_reports

    # TODAY
    def getTodayReportsHot(self, parameters):
        tz_delta = parameters['tz_delta']
        pk = parameters['pk']
        frt = parameters['frt']
        hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk, frt)
            )
        # import ipdb;ipdb.set_trace()
        return hot_reports

    def getTodayReports(self, parameters):
        tz_delta = parameters['tz_delta']
        str_pk = parameters['str_pk']
        correct_limit_from = parameters['correct_limit_from']
        correct_limit_count = parameters['correct_limit_count']
        pk = parameters['pk']
        frt = parameters['frt']

        simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt)
            )
        return simple_reports