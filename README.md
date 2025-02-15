# pymysql

pymysql hands-on 실습입니다.

## 개요

jolse 사이트를 크롤링, pymysql을 이용해서 데이터를 mysql에 넣습니다.

## pymysql 문법

**db, cursor 등록**

```
db = pymysql.connect(host, port, user, passwd, charset)
cursor = db.cursor()
```

**sql 실행**

```
sql = f"insert into products (datas)
values = datas
cursor.execute(sql, values)
db.commit()
```

**db 종료**

```
db.close()
```

## 실행

**1. Clone repository**

```
git clone https://github.com/AlpacaMale/pymysql
```

**2. Change working directory**

```
cd pymysql
```

**3. Install dependency**

```
pip install -r requirements.txt
```

**4. Write your env setup**

```
URL='https://jolse.com/category/toners-mists/1019/?page='
```

**5. Execute main.py**

```
python main.py
```
