# haohua-spider
这个仓库是爬虫小白的一个练手仓库，爬取了好花网(`https://www.haohua.com/`)首页的商品内容，可对爬取的信息进行分类处理，并同时存储到excel表与SQLite库中

##项目说明
本项目为爬虫入门练习，主要练习以下内容:
- 使用 `requests` 发送请求，获取页面 HTML
- 使用 `BeautifulSoup` 解析页面，提取专区信息和商品数据
- 按专区对数据进行分类整理
- 使用 `pandas` 将数据写入 Excel 的不同 sheet
- 使用 `sqlite3` 将数据存入 SQLite 数据库

##环境要求
- Python 3.x
- requests
- beautifulsoup4
- pandas
- openpyxl

##安装依赖
在终端运行
pip install requests beautifulsoup4 pandas openpyxl

##运行方式
安装后在对应路径终端运行python obj_2.py即可
运行完成后会生成对应的excel表与db文件
