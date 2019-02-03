# ETU Exam Time Table
This repository contains a helper API server for our senior project [ABC-Mirror](https://github.com/ETU-ABC/ABC-Mirror).

Live demo can be found [here](https://lit-brushlands-65739.herokuapp.com/).

## Available Endpoints

### ``` GET /```

Returns all the exams in the database in JSON format.

#### Response


    [
      {
        "course_code": "PSİ 341",
        "course_name": "Gelişim Psikolojisi: Yetişkinlik ve yaşlılık",
        "exam_date": "29/01/2019",
        "exam_day": "Salı",
        "exam_time": "16:30-18:20"
      },
      {
        "course_code": "PSİ 312",
        "course_name": "Kişilik Kuramları",
        "exam_date": "31/01/2019",
        "exam_day": "Perşembe",
        "exam_time": "09:30-11:20"
      },
      .
      .
      .
    ]

### ``` GET /exam/<course_code>```
Returns all the exams(may be more than one) of the given ```course_code``` in JSON format.

#### Response
``` GET /exam/BİL 361```



    [
      {
        "course_code": "BİL 361",
        "course_name": "Bilgisayar Mimarisi ve Organizasyonu",
        "exam_date": "06/02/2019",
        "exam_day": "Çarşamba",
        "exam_time": "18:30-20:20"
      },
      {
        "course_code": "BİL 361",
        "course_name": "Bilgisayar Mimarisi ve Organizasyonu",
        "exam_date": "04/03/2019",
        "exam_day": "Pazartesi",
        "exam_time": "08:30-10:20"
      }
    ]


