class Templates:
    class QuickReplies:
        after_action = [
            {
                'content_type': 'text',
                'title': '๊ตฟ!๐',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐๋์๋ง ๋ณด๊ธฐ',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐พ์์ค ์ฝ๋ ๋ณด๊ธฐ',
                'payload': '',
                'image_url': ''
            }
        ]

        after_meal = [
            {
                'content_type': 'text',
                'title': '์์์ ์ ๋ณด ๋ณด๊ธฐ',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '์ค๋ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๋ด์ผ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๊ตฟ!๐',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐พ์์ค ์ฝ๋ ๋ณด๊ธฐ',
                'payload': '',
                'image_url': ''
            }
        ]

        after_nutrition = [
            {
                'content_type': 'text',
                'title': '์ค๋ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๋ด์ผ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๊ตฟ!๐',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐พ์์ค ์ฝ๋ ๋ณด๊ธฐ',
                'payload': '',
                'image_url': ''
            }
        ]

        default = [
            {
                'content_type': 'text',
                'title': '์ค๋ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๋ด์ผ ๊ธ์',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๊ตฟ!๐',
                'payload': '',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐๋์๋ง ๋ณด๊ธฐ',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐พ์์ค ์ฝ๋ ๋ณด๊ธฐ',
                'payload': '',
                'image_url': ''
            }
        ]

        intro = [
            {
                'content_type': 'text',
                'title': '๊ทธ๋!๐',
                'payload': 'INTRO_MORE',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๋๊ณ , ์ฌ์ฉ๋ฒ์ด๋ ์๋ ค์ค.',
                'payload': 'HELP',
                'image_url': ''
            }
        ]

        after_user_error = [
            {
                'content_type': 'text',
                'title': '๐๋์๋ง ๋ณด๊ธฐ',
                'payload': 'HELP',
                'image_url': ''
            },
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            }
        ]

        after_system_error = [
            {
                'content_type': 'text',
                'title': '๐จ๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
                'payload': 'BUGREPORT',
                'image_url': ''
            }
        ]

    class Cards:
        intro_features = [
            {
                'title': '๋ ๊น์งํ  ์ ๊ธ์ ๊ฐ์ ธ์ค๊ธฐ',
                'image_url': '%rootdir%/static/meal.jpg',
                'subtitle': '์ ๊ตญ ์ด์ค๊ณ ์ ๊ธ์์ ๋ ๊น์งํ  ์์ ๊ฐ์ ธ์ฌ ์ ์์ด์. ์ฑ ์์ด๋์!',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '์ด๋ป๊ฒ ์ฐ๋์ง ๋ณด๊ธฐ',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '์๋ฌ์ง ์ ๋ณด',
                'image_url': '%rootdir%/static/allergy.jpg',
                'subtitle': '์๋ฌ์ง๊ฐ ์์ผ์๋ ๊ฑฑ์  ๋ง์ธ์. ๊ธ์๋ด์ด ์์์ ์ฑ๊ฒจ ์ค ๊ฑฐ์์.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '์ด๋ป๊ฒ ์ฐ๋์ง ๋ณด๊ธฐ',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '์์์ ์ ๋ณด',
                'image_url': '%rootdir%/static/nutrients.png',
                'subtitle': '์ด์ฐ ๊ฑฑ์ ์ NO! ๊ธ์์ ์์์ ์ ๋ณด๋ฅผ ๊ธ์๋ด์์ ๋ณผ ์ ์์ด์.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '์ด๋ป๊ฒ ์ฐ๋์ง ๋ณด๊ธฐ',
                        'payload': 'HELP'
                    }
                ]
            },
            {
                'title': '[์ค๋น์ค] ๊ธ์ ๊ตฌ๋',
                'image_url': '%rootdir%/static/newspaper.jpg',
                'subtitle': '(์ค๋น์ค) ์ง์ ํ ์๊ฐ๋ง๋ค ๋งค์ผ ๊ธ์ ์๋ฆผ์ ๋ฐ์๋ณด์ค ์ ์์ด์.',
                'buttons': [
                    {
                        'type': 'postback',
                        'title': '[๐งช ๊ณง ์ฐพ์์ต๋๋ค!]',
                        'payload': 'PLACEHOLDER'
                    }
                ]
            }
        ]

        bug_report = [{
            'title': '๋ฒ๊ทธ ์ ๊ณ ํ๊ธฐ',
            'image_url': '%rootdir%/static/siren.png',
            'subtitle': '์๋ ๋ฒํผ์ ํด๋ฆญํ๋ฉด ๋ฒ๊ทธ ์ ๊ณ  ์์์ผ๋ก ์ฐ๊ฒฐ๋ฉ๋๋ค.',
            'buttons': [
                {
                    'type': 'web_url',
                    'url': '%rootdir%/support/bugreport?id=',
                    'title': '๋ฒ๊ทธ ์ก์ผ๋ฌ ๊ฐ๊ธฐ'
                }
            ]
        }]

        view_source = [
            {
                'title': '๊นํ๋ธ์์ ์์ค ๋ณด๊ธฐ',
                'image_url': '%rootdir%/static/github-universe.jpg',
                'subtitle': 'Github์์ ๊ธ์๋ด5์ ์์ค ์ฝ๋๋ฅผ ๋ณด์ค ์ ์์ด์.',
                'buttons': [
                    {
                        'type': 'web_url',
                        'url': 'https://github.com/dazzleofficial/mealworm5',
                        'title': '์์ค ์ฝ๋ ๋ณด๊ธฐ'
                    }
                ]
            }
        ]
