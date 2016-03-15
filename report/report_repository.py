from places.models import Place


class ReportRepository():

    # TODAY
    def getTodayReportsHot(self, parameters):
        tz_delta = parameters['tz_delta']
        frt = parameters['frt']
        city_pk = parameters['city_pk']
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
                    'COUNT(l.id) as like_cnt, '
                    'p.city_id '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'LEFT JOIN places_place p ON p.id = report_report.place_id '

                'WHERE report_report.enable = 1 '
                'AND p.city_id = %s '
                'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (city_pk, frt)
            )
        # import ipdb;ipdb.set_trace()
        return hot_reports

    def getTodayReports(self, parameters):
        tz_delta = parameters['tz_delta']
        str_pk = parameters['str_pk']
        correct_limit_from = parameters['correct_limit_from']
        correct_limit_count = parameters['correct_limit_count']
        frt = parameters['frt']
        city_pk = parameters['city_pk']

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
                    'COUNT(l.id) as like_cnt, '
                    'p.city_id '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'LEFT JOIN places_place p ON p.id = report_report.place_id '

                 'WHERE report_report.enable = 1 '
                 'AND p.city_id = %s '
                 'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (city_pk, frt)
            )
        return simple_reports
