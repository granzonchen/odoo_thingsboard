# -*- coding: utf-8 -*-

import base64
import json
import logging
import datetime
import werkzeug

from odoo import http
from odoo.http import request, JsonRequest

_logger = logging.getLogger(__name__)


class AntaiDataRoute(http.Controller):
    
    @http.route('/adc/dingdan', type='http', methods=['POST','GET'], auth="none", csrf=False, cors="*")
    def adc_dingdan(self, **kwargs):
        """
        大屏 - 订单
        """
        results = request.env['adc.mes.sale.order'].sudo().get_adc_dingdan()
        
        return json.dumps(results)
    
    @http.route('/adc/chanliang', type='http', methods=['POST','GET'], auth="none", csrf=False, cors="*")
    def adc_chanliang(self, **kwargs):
        """
        总览大屏 - 产量
        后端： 大屏 - 公司级 - 生产产量
        """
        results = request.env['adc.shengchan'].sudo().get_total_chanliang()
        return json.dumps({'data':results})

    @http.route('/adc/plan', type='http', methods=['POST','GET'], auth="none", csrf=False, cors="*")
    def adc_plan(self, **kwargs):
        """
        主计划按日按月，分计划按日按月
        {
            'main_plan_day': [
                {'day': '2021-10-02', 'rate': 80.6}
                {'day': '2021-10-03', 'rate': 87.0}
            ], 
            'main_plan_month': [
                {'day': '2021-10', 'rate': 90},
                {'day': '2021-11', 'rate': 87},
            ], 
            'plan_day': [
                {'day': '2021-10-02', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
                {'day': '2021-10-03', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
            ], 
            'plan_month': [
                {'day': '2021-10', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
                {'day': '2021-11', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
            ]
        }

        'plan_month': {
            'material': [
                {'day': '2021-10', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
                {'day': '2021-11', 'cailiao': 80, 'diandu': 90, 'jiagong': 76, 'jianbao': 67}
            ],
            'machining': [

            ],
            'plating': [

            ],
            'packing': [

            ]
        }
        """
        # FIXME: 以后根据需求添加时间限制
        orders = request.env['adc.plan.rate'].sudo().search_read(
            [['type', '=', 'major']],
            ["date", "month", "year", "type", "ontime", "count", "rate"],
            order="date asc"
        )
        
        main_plan_day = []
        main_plan_month = []
        _main_plan_month = {}
        
        for order in orders:
            _date = order['date'].strftime("%Y-%m-%d")
            main_plan_day.append({
                'rate': order['rate'],
                'done': order['ontime'],
                'all': order['count'],
                'day': _date
            })

            
            _month = order['month']   # 21-10
            if _month not in _main_plan_month:
                _main_plan_month[_month] = {
                    'done': order['ontime'],
                    'all': order['count']
                }
            else:
                _main_plan_month[_month].update({
                    'done': order['ontime'] + _main_plan_month[_month]['done'],
                    'all': order['count'] + _main_plan_month[_month]['all'],
                })
        
        for k,v in _main_plan_month.items():
            main_plan_month.append({
                'rate': round(v['done'] / float(v['all']) * 100,2),
                'done': v['done'],
                'all': v['all'],
                'day': k
            })
        
        # _logger.info(f"=============main_plan_day: {main_plan_day}")
        # _logger.info(f"=============main_plan_month: {main_plan_month}")
        
        orders = request.env['adc.plan.rate'].sudo().search_read(
            [['type', '!=', 'major']],
            ["date", "month", "year", "type", "ontime", "count", "rate"],
            order="date asc"
        )
        
        plan_day_dic = {
            'material': [],
            'machining': [],
            'plating': [],
            'packing': []
        }
        
        for order in orders:
            # {'__count': 1, 'ontime': 27, 'count': 34, 'rate': 79, 'date:day': '14 Sep 2022', 'type': 'machining', 
            # '__domain': ['&', '&', ('date', '>=', '2022-09-14'), ('date', '<', '2022-09-15'), ('type', '=', 'machining')]}
            _done = 0
            _all = 0
            plan_day_dic[order['type']].append({
                'rate': order['rate'],
                'done': order['ontime'],
                'all': order['count'],
                'day': order['date'].strftime("%Y-%m-%d")
            })
        
        plan_month_dic = {
            'material': [],
            'machining': [],
            'plating': [],
            'packing': []
        }

        orders = request.env['adc.plan.rate'].sudo().search_read(
            [['type', '!=', 'major']],
            ["date", "month", "year", "type", "ontime", "count", "rate"],
            order="date asc"
        )

        material = {}
        machining = {}
        plating = {}
        packing = {}

        for order in orders:
            _month = order['month']
            if order['type'] == "material":
                if order['month'] not in material:
                    material[_month] = {
                        'done': order['ontime'],
                        'all': order['count']
                    }
                else:
                    material[_month].update({
                        'done': order['ontime'] + material[_month]['done'],
                        'all': order['count'] + material[_month]['all']
                    })
            
            if order['type'] == "machining":
                if order['month'] not in machining:
                    machining[_month] = {
                        'done': order['ontime'],
                        'all': order['count']
                    }
                else:
                    machining[_month].update({
                        'done': order['ontime'] + machining[_month]['done'],
                        'all': order['count'] + machining[_month]['all']
                    })
            
            if order['type'] == "plating":
                if order['month'] not in plating:
                    plating[_month] = {
                        'done': order['ontime'],
                        'all': order['count']
                    }
                else:
                    plating[_month].update({
                        'done': order['ontime'] + plating[_month]['done'],
                        'all': order['count'] + plating[_month]['all']
                    })

            if order['type'] == "packing":
                if order['month'] not in packing:
                    packing[_month] = {
                        'done': order['ontime'],
                        'all': order['count']
                    }
                else:
                    packing[_month].update({
                        'done': order['ontime'] + packing[_month]['done'],
                        'all': order['count'] + packing[_month]['all']
                    })
            
        for k,v in material.items():
            plan_month_dic['material'].append({
                'rate': round(v['done'] / float(v['all']) * 100,2),
                'done': v['done'],
                'all': v['all'],
                'day': k
            })
        
        for k,v in machining.items():
            plan_month_dic['machining'].append({
                'rate': round(v['done'] / float(v['all']) * 100,2),
                'done': v['done'],
                'all': v['all'],
                'day': k
            })
        
        for k,v in plating.items():
            plan_month_dic['plating'].append({
                'rate': round(v['done'] / float(v['all']) * 100,2),
                'done': v['done'],
                'all': v['all'],
                'day': k
            })

        for k,v in packing.items():
            plan_month_dic['packing'].append({
                'rate': round(v['done'] / float(v['all']) * 100,2),
                'done': v['done'],
                'all': v['all'],
                'day': k
            })
        

        return json.dumps({
            'main_plan_day': main_plan_day,
            'main_plan_month': main_plan_month,
            'plan_day': plan_day_dic,
            'plan_month': plan_month_dic
        })
    
    