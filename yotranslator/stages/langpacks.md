# Языковые пакеты
Ё поддерживает перевод ключевых слов на другие языки. Для того чтобы
слова были переведены нужно чтобы:
1. В файле basic.yolp были написаны нужные переводы
2. Ё поддерживал выбранный язык

Языковые настройки хранятся в файле *basic.yolp*. Он устроен как обычный json.

    {
      "ключевое слово":
      {
        "язык": "перевод",
        "другой язык": "другой перевод"
      }
    }

Этот файл лежит в корневой директории среды разработки и транслятора и доступен
для редактирования.