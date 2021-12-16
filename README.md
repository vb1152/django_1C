# Order

Order app helps me to create and send orders in excel files to its producers.

## Explanation

I run small grocery shop. Every day I fill (create) excel files and send them to food manufacturers to order some goods. Further I will use [SCU](https://en.wikipedia.org/wiki/Stock_keeping_unit) term, when talking about goods. In the shop I use [1C program](https://en.wikipedia.org/wiki/1C:Enterprise) with its own database and configurations. However, this program was designed and created in 90's and for large companies. So with python and Django I decided to automate some processes in my daily work.

## Distinctiveness and Complexity

In my db I use 8 main models for data and several help models (forms, tables etc.).

On main page app has two buttons, navbar navigation links and 1c connection label. When label is green - connection to 1C db is active.

Connection.
Connection to 1C db created via [OData](https://www.odata.org/) and [Apache](https://httpd.apache.org/). 1C and Apache are installed on the same computer. [Details_1_eng](https://support.1ci.com/hc/en-us/articles/360018953834-Methods-of-integration-with-1C-Enterprise-applications), [Details_2_rus](https://infostart.ru/1c/articles/711302/), [Details_3_rus](https://its.1c.ru/db/fresh#content:19956692:1:issogl1_hs0nuvj).

![Main page](/images/main.png)

Producers' page has button 'Update vendors' via which it is possible to check 1C db for new producers. After button, we can see how many producers saved in apps db. Then forms with buttons where located clean files from manufacturers and ready to send files. Below that there is [jsGrid](http://js-grid.com/) responsive table to see and modify data about producers. To start work with producer I put tick, save min sum for order, email to send order files, files to fill from producers (if needed), column with barcodes in those files from producers and column to write data order.
![Producers](/images/producers.png)

ABC page. Form with buttons to choose dates. Then via OData request, we get sales for a specified period. After that we calculate [ABC](https://en.wikipedia.org/wiki/ABC_analysis) classes for SCU and save that information to db.
![ABC](/images/abc.png)

Sheet page. List of SCU with sales and stock data with ABC classes. Only for information purpose.

Insurance reserves. jsGrid table with list of SCU grouped hierarchically, SCU's ABC class and data about insurance reserves, max order, multiplicity and max stock. I use this data to calculate order for every SCU. Formula to calculate: order = SCU_Expense + safe_stock - SCU_ClosingBalance. If the order must be multiple: order = ((order // multipl) + 1 ) * multipl.
![insurance reserves](/images/reserves.png)

1C settings. Form with settings to connect to 1C db.
![1c](/images/1c.png)

Data management. Buttons for data control. Load and delete folders, SCU, barcodes, prices.
![Data](/images/data.png)

Order page. Page has only list of buttons for producers, which are active and work with my shop. When some button clicked, order is calculating and creating (or filling) excel files
![order1](/images/order1.png)
![order2](/images/order2.png)
