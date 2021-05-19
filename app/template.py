class Templates:
    class QuickReplies:
        after_action = [
            {
                'content_type': 'text',
                'title': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '📚도움말 보기',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        after_meal = [
            {
                'content_type': 'text',
                'title': '영양소 정보 보기',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '오늘 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '내일 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        after_nutrition = [
            {
                'content_type': 'text',
                'title': '오늘 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '내일 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        default = [
            {
                'content_type': 'text',
                'title': '오늘 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '내일 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '📚도움말 보기',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        intro = [
            {
                'content_type': 'text',
                'title': '그래!😉',
                'payload': 'INTRO_MORE',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '됐고, 사용법이나 알려줘.',
                'payload': 'HELP',
                'image_url': ''
            }
        ]

        after_user_error = [
            {
                'content_type': 'text',
                'title': '📚도움말 보기',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            }
        ]

        after_system_error = [
            {
                'content_type': 'text',
                'title': '🚨버그 신고하기',
                'payload': 'BUGREPORT',
                'image_url': ''
            }
        ]

    class Cards:
        intro_features = [
            {
                'title': '눈 깜짝할 새 급식 가져오기',
                'image_url': '%rootdir%/static/meal.jpg',
                'subtitle': '전국 초중고의 급식을 눈 깜짝할 새에 가져올 수 있어요. 앱 없이도요!',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '어떻게 쓰는지 보기',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '알러지 정보',
                'image_url': '%rootdir%/static/allergy.jpg',
                'subtitle': '알러지가 있으셔도 걱정 마세요. 급식봇이 알아서 챙겨 줄 거에요.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '어떻게 쓰는지 보기',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '영양소 정보',
                'image_url': '%rootdir%/static/nutrients.png',
                'subtitle': '살찔 걱정은 NO! 급식의 영양소 정보를 급식봇에서 볼 수 있어요.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '어떻게 쓰는지 보기',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '[준비중] 급식 구독',
                'image_url': '%rootdir%/static/newspaper.jpg',
                'subtitle': '(준비중) 지정한 시간마다 매일 급식 알림을 받아보실 수 있어요.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '[🧪 곧 찾아옵니다!]',
                        'payload': 'PLACEHOLDER'
                    }
                ]
            }
        ]

        bug_report = [{
            'title': '버그 신고하기',
            'image_url': '%rootdir%/static/siren.png',
            'subtitle': '아래 버튼을 클릭하면 버그 신고 양식으로 연결됩니다.',
            'buttons': [
                {
                    'type': 'web_url',
                    'url': '%rootdir%/support/bugreport?id=',
                    'title': '버그 잡으러 가기'
                }
            ]
        }]

        view_source = [
            {
                'title': '깃허브에서 소스 보기',
                'image_url': '%rootdir%/static/github-universe.jpg',
                'subtitle': 'Github에서 급식봇5의 소스 코드를 보실 수 있어요.',
                'buttons': [
                    {
                        'type': 'web_url',
                        'url': 'https://github.com/dazzleofficial/mealworm5',
                        'title': '소스 코드 보기'
                    }
                ]
            }
        ]
