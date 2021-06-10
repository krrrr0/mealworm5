# 급식봇 API 서버 버전 5
<a href="https://m.me/mealworm05">![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger&logoColor=%23ffffff)</a>
![GitHub](https://img.shields.io/badge/LICENSE-WTFPL-blueviolet?style=for-the-badge)
  
<img src="https://user-images.githubusercontent.com/30792695/82785254-2f5e8880-9e9d-11ea-8f34-dd2e7542bde7.png" alt="급식봇 로고" width="30%">


## 개요
급식봇은 자연어 인식 기술을 활용한 인공지능 급식 챗봇입니다!  
2021년부터 [@dazzleofficial](https://github.com/dazzleofficial/) 에서 운영이 이루어지고 있습니다.  
  
불쾌감을 느낄 수 있는 상당히 더러운 코드가 포함되어 있으니 시청에 주의를 요합니다.

## 특징
**급식봇은 자연어 인식 기술을 활용하여 정형화되지 않은 대화에서 사용자의 의도를 추출해 급식을 가져옵니다.**  
급식봇으로는 전국의 초/중/고등학교의 급식, 알러지 정보 등을 페이스북 메신저 플랫폼을 통해 빠르고 쉽게 조회하실 수 있습니다.

급식봇은 Python, Flask 프레임워크와 Jinja2 템플릿 엔진, 그리고 Dialogflow를 이용해 만들어졌습니다.  
2019년부터 [나이스 오픈API](https://open.neis.go.kr/portal/mainPage.do)가 개방되면서 급식 조회 시에 나이스 API를 사용합니다.

## 사용법
<a href="https://m.me/mealworm05">![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger&logoColor=%23ffffff)</a>  
위 버튼을 눌러 시작합니다. 페이스북 메신저를 이용하기 위해서는 페이스북 계정이 필요합니다.  
⚠ 주의: 메신저 라이트를 이용중이신 경우 정상적으로 표시되지 않는 요소들이 있을 수 있습니다.  
  
`급식봇 내일 서울과고 급식` --> 내일의 서울과학고 중식을 가져옵니다  
`세종과학고 3월 14일 저녁 알려줘라` --> 3월 14일의 세종과학고 석식을 가져옵니다  
`내일은?` --> 앞서 요청했던 학교의 내일 중식을 가져옵니다

날짜를 생략할 경우 기본값은 오늘, 학교 이름을 생략할 경우 기본값은 마지막에 요청했던 학교, 
밥타임(?)을 생략할 경우 기본은 중식을 가져옵니다.

## 피드백
급식봇 내부의 '버그 신고하기' 기능을 통해 의견이나 개선사항을 건의하실 수 있습니다.  
<contact (골뱅이) dazzle.works> 로 이메일을 보내시면 더 빠른 처리를 기대하실 수 있습니다.  
  
급식봇이 도움이 되셨다면 친구들과 공유하고 페이지 좋아요를 눌러주세요!

## 라이선스
mealworm5 코드는 [WTFPL](http://www.wtfpl.net/) (Do What The Fuck You Want To Public License) 로 배포됩니다.
  