# PHP 速查笔记

## 怎么用这份文件

这份笔记覆盖**从小白到精通**的 PHP：基础语法 → 类型与运算符 → 字符串与正则 → 数组 → 流程控制 → 函数 → 面向对象 → 错误处理 → 文件 → 表单与超全局变量 → 会话 → 数据库 → 时间/JSON/加密 → 安全危险函数，供忘记时速查，也够系统学一遍。
每个条目格式一样：**解析**（这东西是干什么的，白话 2~4 句）→ **操作**（一段能直接跑的示例，末尾 `// 运行结果` 是真跑出来的输出）→ `> ⚠️`（坑和易错点，没有就不写）。
带 🔒 的是**安全相关**条目——Web 渗透会直接用到，解析里都会点明"为什么危险 / 怎么被利用"。
所有示例都在**本机真环境实跑**：PHP **8.5.11**（`/opt/homebrew/bin/php`）；超全局变量（`$_GET`/`$_POST`/`$_COOKIE`/`$_FILES`/`$_SESSION` 等）用本机 `php -S` 起服务 + `curl` 真实请求；数据库条目真连本机 **MySQL 8.4.11** 的 `php_demo` 库。所以每条 `// 运行结果` 都是现场输出，不是编的。
读法：先看索引跳到你要的那条，看不懂再顺着分类从前往后读。章节顺序就是学习顺序：

一 基础语法与输出 → 二 数据类型与运算符 → 三 字符串与正则 → 四 数组与常用函数 → 五 流程控制 → 六 函数 → 七 面向对象 → 八 错误与异常处理 → 九 文件与目录操作 → 十 表单与超全局变量（Web 请求） → 十一 会话与 Cookie → 十二 数据库操作 → 十三 时间、JSON 与加密 → 十四 危险函数（渗透必看）

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| 一 基础语法与输出 | [`<?php`](#php-起止标签与代码块) | 起止标签与代码块 |
| 一 基础语法与输出 | [`注释`](#注释-三种注释写法) | 三种注释写法 |
| 一 基础语法与输出 | [`echo`](#echo-输出内容最常用) | 输出内容（最常用） |
| 一 基础语法与输出 | [`print`](#print-输出内容并返回-1) | 输出内容并返回 1 |
| 一 基础语法与输出 | [`print_r 与 var_dump`](#print_r-与-var_dump-打印变量的类型和结构) | 打印变量的类型和结构 |
| 一 基础语法与输出 | [`变量`](#变量-用美元符号开头存数据) | 用美元符号开头存数据 |
| 一 基础语法与输出 | [`常量`](#常量-定义后不能改的值) | 定义后不能改的值 |
| 一 基础语法与输出 | [`heredoc 与 nowdoc`](#heredoc-与-nowdoc-多行字符串的两种写法) | 多行字符串的两种写法 |
| 一 基础语法与输出 | [`类型声明与严格模式`](#类型声明与严格模式-给参数和返回值标类型) | 给参数和返回值标类型 |
| 一 基础语法与输出 | [`魔术常量`](#魔术常量-随位置自动变化的预定义常量) | 随位置自动变化的预定义常量 |
| 二 数据类型与运算符 | [`字符串`](#字符串-单引号与双引号的区别) | 单引号与双引号的区别 |
| 二 数据类型与运算符 | [`字符串拼接`](#字符串拼接-用点号连接) | 用点号连接 |
| 二 数据类型与运算符 | [`数据类型`](#数据类型-八种类型速览) | 八种类型速览 |
| 二 数据类型与运算符 | [`类型转换`](#类型转换-显式与隐式转换) | 显式与隐式转换 |
| 二 数据类型与运算符 | [`类型判断函数`](#类型判断函数-用-is_-系列判断类型) | 用 is_ 系列判断类型 |
| 二 数据类型与运算符 | [`==与===`](#与-弱比较与严格比较) 🔒 | 弱比较与严格比较 |
| 二 数据类型与运算符 | [`算术运算符`](#算术运算符-加减乘除取余) | 加减乘除取余 |
| 二 数据类型与运算符 | [`赋值与自增自减`](#赋值与自增自减-复合赋值与自增自减) | 复合赋值与自增自减 |
| 二 数据类型与运算符 | [`逻辑运算符`](#逻辑运算符-与或非的短路求值) | 与或非的短路求值 |
| 二 数据类型与运算符 | [`位运算符`](#位运算符-按位运算) | 按位运算 |
| 二 数据类型与运算符 | [`null 与 isset、empty`](#null-与-issetempty-判断变量是否设置或为空) 🔒 | 判断变量是否设置或为空 |
| 三 字符串与正则 | [`常用字符串函数`](#常用字符串函数-长度大小写截取与替换) | 长度、大小写、截取与替换 |
| 三 字符串与正则 | [`mb_ 系列函数`](#mb_-系列函数-正确按字数处理中文) | 正确按字数处理中文 |
| 三 字符串与正则 | [`sprintf`](#sprintf-格式化字符串) | 格式化字符串 |
| 三 字符串与正则 | [`str_pad、str_repeat、strrev`](#str_padstr_repeatstrrev-补位重复与反转) | 补位、重复与反转 |
| 三 字符串与正则 | [`explode 与 implode`](#explode-与-implode-字符串与数组互转) | 字符串与数组互转 |
| 三 字符串与正则 | [`preg_match`](#preg_match-正则单次匹配) 🔒 | 正则单次匹配 |
| 三 字符串与正则 | [`preg_match_all`](#preg_match_all-正则全部匹配) 🔒 | 正则全部匹配 |
| 三 字符串与正则 | [`preg_replace`](#preg_replace-正则查找替换) 🔒 | 正则查找替换 |
| 三 字符串与正则 | [`正则元字符`](#正则元字符-常用元字符与修饰符速查) | 常用元字符与修饰符速查 |
| 四 数组与常用函数 | [`数组`](#数组-索引数组) | 索引数组 |
| 四 数组与常用函数 | [`关联数组`](#关联数组-键值对) | 键值对 |
| 四 数组与常用函数 | [`多维数组`](#多维数组-嵌套数组) | 嵌套数组 |
| 四 数组与常用函数 | [`foreach 遍历`](#foreach-遍历-遍历数组) | 遍历数组 |
| 四 数组与常用函数 | [`常用数组函数`](#常用数组函数-计数增删与查找) | 计数、增删与查找 |
| 四 数组与常用函数 | [`排序函数`](#排序函数-sortasortksortusort) | sort、asort、ksort、usort |
| 四 数组与常用函数 | [`array_map、array_filter、array_reduce`](#array_maparray_filterarray_reduce-用回调处理数组) | 用回调处理数组 |
| 四 数组与常用函数 | [`array_merge`](#array_merge-合并数组的两种区别) | 合并数组的两种区别 |
| 四 数组与常用函数 | [`array_column、array_keys、array_values`](#array_columnarray_keysarray_values-取列与取键值) | 取列与取键值 |
| 四 数组与常用函数 | [`in_array 与 array_search`](#in_array-与-array_search-查找元素是否存在) 🔒 | 查找元素是否存在 |
| 四 数组与常用函数 | [`array_slice 与 array_splice`](#array_slice-与-array_splice-截取与移除替换) | 截取与移除替换 |
| 四 数组与常用函数 | [`list 与数组解构`](#list-与数组解构-解构赋值) | 解构赋值 |
| 五 流程控制 | [`if、else if、else`](#ifelse-ifelse-条件分支) | 条件分支 |
| 五 流程控制 | [`switch、case`](#switchcase-多路分支) 🔒 | 多路分支 |
| 五 流程控制 | [`match 表达式`](#match-表达式-值匹配并返回php-8) | 值匹配并返回（PHP 8） |
| 五 流程控制 | [`for 循环`](#for-循环-已知次数的循环) | 已知次数的循环 |
| 五 流程控制 | [`while、do-while`](#whiledo-while-条件循环) | 条件循环 |
| 五 流程控制 | [`break 与 continue`](#break-与-continue-跳出与跳过) | 跳出与跳过 |
| 五 流程控制 | [`三元运算符与空合并`](#三元运算符与空合并-一行判断与给默认值) | 一行判断与给默认值 |
| 五 流程控制 | [`替代语法`](#替代语法-模板里的-if-和-for-写法) | 模板里的 if 和 for 写法 |
| 六 函数 | [`函数定义与调用`](#函数定义与调用-把逻辑打包复用) | 把逻辑打包复用 |
| 六 函数 | [`函数参数与返回值`](#函数参数与返回值-默认值与引用传参) | 默认值与引用传参 |
| 六 函数 | [`可变参数与参数解包`](#可变参数与参数解包-收不定个数的参数) | 收不定个数的参数 |
| 六 函数 | [`匿名函数与闭包`](#匿名函数与闭包-没有名字的函数) | 没有名字的函数 |
| 六 函数 | [`箭头函数`](#箭头函数-一行式闭包php-74) | 一行式闭包（PHP 7.4+） |
| 六 函数 | [`变量作用域`](#变量作用域-局部全局与-static) 🔒 | 局部、全局与 static |
| 六 函数 | [`递归函数`](#递归函数-函数调用自己) | 函数调用自己 |
| 六 函数 | [`变量函数与 call_user_func`](#变量函数与-call_user_func-用字符串变量调用函数) 🔒 | 用字符串/变量调用函数 |
| 七 面向对象 | [`类与对象`](#类与对象-定义类并实例化) | 定义类并实例化 |
| 七 面向对象 | [`类常量与属性`](#类常量与属性-类里的变量和固定值) | 类里的变量和固定值 |
| 七 面向对象 | [`构造与析构函数`](#构造与析构函数-创建与销毁对象时自动调用) 🔒 | 创建与销毁对象时自动调用 |
| 七 面向对象 | [`继承`](#继承-用-extends-复用父类) | 用 extends 复用父类 |
| 七 面向对象 | [`访问控制`](#访问控制-publicprotectedprivate) | public、protected、private |
| 七 面向对象 | [`静态成员`](#静态成员-static-与-self) | static 与 self、:: |
| 七 面向对象 | [`抽象类与接口`](#抽象类与接口-abstract-与-interface) | abstract 与 interface |
| 七 面向对象 | [`魔术方法`](#魔术方法-被特殊触发的方法) 🔒 | 被特殊触发的方法 |
| 七 面向对象 | [`命名空间`](#命名空间-隔离同名的类与函数) | 隔离同名的类与函数 |
| 七 面向对象 | [`trait`](#trait-横向复用方法) | 横向复用方法 |
| 八 错误与异常处理 | [`错误报告`](#错误报告-打开与关闭报错) 🔒 | 打开与关闭报错 |
| 八 错误与异常处理 | [`try、catch、finally`](#trycatchfinally-捕获异常与收尾) | 捕获异常与收尾 |
| 八 错误与异常处理 | [`throw`](#throw-按类型抛出异常) | 按类型抛出异常 |
| 八 错误与异常处理 | [`自定义异常类`](#自定义异常类-继承-exception-定义错误) | 继承 Exception 定义错误 |
| 八 错误与异常处理 | [`set_error_handler`](#set_error_handler-把错误变成自定义处理) | 把错误变成自定义处理 |
| 八 错误与异常处理 | [`error_log`](#error_log-把错误写进日志文件) | 把错误写进日志文件 |
| 九 文件与目录操作 | [`文件读写函数`](#文件读写函数-整文件读与写) 🔒 | 整文件读与写 |
| 九 文件与目录操作 | [`fopen、fwrite、fread、fclose`](#fopenfwritefreadfclose-按句柄打开读写关闭) | 按句柄打开读写关闭 |
| 九 文件与目录操作 | [`file`](#file-把文件按行读成数组) | 把文件按行读成数组 |
| 九 文件与目录操作 | [`文件与目录函数`](#文件与目录函数-判断删除建目录列目录) | 判断、删除、建目录、列目录 |
| 九 文件与目录操作 | [`include 与 require`](#include-与-require-文件包含) 🔒 | 文件包含 |
| 九 文件与目录操作 | [`路径处理`](#路径处理-拆解文件路径) 🔒 | 拆解文件路径 |
| 九 文件与目录操作 | [`glob`](#glob-按通配符查找文件) | 按通配符查找文件 |
| 九 文件与目录操作 | [`读写 JSON 文件`](#读写-json-文件-结构化数据存盘) | 结构化数据存盘 |
| 十 表单与超全局变量（Web 请求） | [`$_GET`](#_get-取地址栏参数) 🔒 | 取地址栏参数 |
| 十 表单与超全局变量（Web 请求） | [`$_POST`](#_post-取表单提交的数据) 🔒 | 取表单提交的数据 |
| 十 表单与超全局变量（Web 请求） | [`$_REQUEST`](#_request-一次取-get-post-cookie) 🔒 | 一次取 GET POST Cookie |
| 十 表单与超全局变量（Web 请求） | [`$_COOKIE`](#_cookie-取浏览器的-cookie) 🔒 | 取浏览器的 Cookie |
| 十 表单与超全局变量（Web 请求） | [`$_SERVER`](#_server-服务器与请求信息) 🔒 | 服务器与请求信息 |
| 十 表单与超全局变量（Web 请求） | [`$_ENV 与环境变量`](#_env-与环境变量-读写环境变量) 🔒 | 读写环境变量 |
| 十 表单与超全局变量（Web 请求） | [`$_FILES`](#_files-接收上传的文件) 🔒 | 接收上传的文件 |
| 十 表单与超全局变量（Web 请求） | [`php://input`](#phpinput-读取原始请求体) 🔒 | 读取原始请求体 |
| 十 表单与超全局变量（Web 请求） | [`filter_var`](#filter_var-校验与过滤输入) 🔒 | 校验与过滤输入 |
| 十 表单与超全局变量（Web 请求） | [`htmlspecialchars`](#htmlspecialchars-输出转义防-xss) 🔒 | 输出转义防 XSS |
| 十一 会话与 Cookie | [`$_SESSION`](#_session-跨页面保存登录状态) 🔒 | 跨页面保存登录状态 |
| 十一 会话与 Cookie | [`session_regenerate_id 与 session_destroy`](#session_regenerate_id-与-session_destroy-换-id-与登出) 🔒 | 换 id 与登出 |
| 十一 会话与 Cookie | [`setcookie`](#setcookie-发送-cookie-给浏览器) 🔒 | 发送 Cookie 给浏览器 |
| 十二 数据库操作 | [`mysqli 连接数据库`](#mysqli-连接数据库-连接-mysql-并查询) 🔒 | 连接 MySQL 并查询 |
| 十二 数据库操作 | [`mysqli 预处理查询`](#mysqli-预处理查询-防-sql-注入mysqli-版) 🔒 | 防 SQL 注入（mysqli 版） |
| 十二 数据库操作 | [`PDO 连接数据库`](#pdo-连接数据库-连接-mysql-并查询pdo-版) 🔒 | 连接 MySQL 并查询（PDO 版） |
| 十二 数据库操作 | [`PDO 预处理查询`](#pdo-预处理查询-防-sql-注入pdo-版) 🔒 | 防 SQL 注入（PDO 版） |
| 十二 数据库操作 | [`PDO 事务`](#pdo-事务-提交与回滚) | 提交与回滚 |
| 十二 数据库操作 | [`查询结果处理`](#查询结果处理-fetch-家族怎么取数据) | fetch 家族怎么取数据 |
| 十三 时间、JSON 与加密 | [`时间函数`](#时间函数-datetimestrtotime) | date、time、strtotime |
| 十三 时间、JSON 与加密 | [`DateTime 类`](#datetime-类-面向对象方式处理日期) | 面向对象方式处理日期 |
| 十三 时间、JSON 与加密 | [`JSON 编解码`](#json-编解码-json_encode-与-json_decode) | json_encode 与 json_decode |
| 十三 时间、JSON 与加密 | [`哈希函数`](#哈希函数-md5sha1-与-password_hash) 🔒 | md5、sha1 与 password_hash |
| 十三 时间、JSON 与加密 | [`对称加密与随机数`](#对称加密与随机数-openssl-加解密与随机数) 🔒 | openssl 加解密与随机数 |
| 十三 时间、JSON 与加密 | [`base64 编码解码`](#base64-编码解码-base64_encode-与-decode) 🔒 | base64_encode 与 decode |
| 十四 危险函数（渗透必看） | [`system`](#system-执行系统命令并直接输出) 🔒 | 执行系统命令并直接输出 |
| 十四 危险函数（渗透必看） | [`exec`](#exec-执行命令只返回最后一行) 🔒 | 执行命令只返回最后一行 |
| 十四 危险函数（渗透必看） | [`shell_exec 与反引号`](#shell_exec-与反引号-执行命令返回全部输出) 🔒 | 执行命令返回全部输出 |
| 十四 危险函数（渗透必看） | [`passthru 与 popen`](#passthru-与-popen-其它命令执行函数) 🔒 | 其它命令执行函数 |
| 十四 危险函数（渗透必看） | [`eval`](#eval-把字符串当代码执行) 🔒 | 把字符串当代码执行 |
| 十四 危险函数（渗透必看） | [`assert`](#assert-断言旧版可当代码执行) 🔒 | 断言（旧版可当代码执行） |
| 十四 危险函数（渗透必看） | [`unserialize`](#unserialize-反序列化字符串成对象) 🔒 | 反序列化字符串成对象 |
| 十四 危险函数（渗透必看） | [`extract 与 parse_str`](#extract-与-parse_str-变量覆盖漏洞) 🔒 | 变量覆盖漏洞 |
| 十四 危险函数（渗透必看） | [`phpinfo`](#phpinfo-信息泄露) 🔒 | 信息泄露 |
| 十四 危险函数（渗透必看） | [`危险函数与超全局变量`](#危险函数与超全局变量-拼接就是漏洞) 🔒 | 拼接就是漏洞 |

---

## 一 基础语法与输出

### `<?php` 起止标签与代码块

**解析**　PHP 代码必须写在 `<?php` 和 `?>` 之间，服务器看到这对标记才把它当代码执行，标记外面的内容会原样输出成 HTML。纯 PHP 文件通常省掉结尾的 `?>`，免得它后面多出一个空行影响输出（本笔记所有示例都这么写）。一个文件里可以有多段 `<?php ... ?>`。

**操作**

```php
<?php echo "第一段 PHP"; ?>
中间这段是纯 HTML
<?php echo "，第二段 PHP"; ?>
// 运行结果：
// 第一段 PHP中间这段是纯 HTML
// ，第二段 PHP
```

### `注释` 三种注释写法

**解析**　注释是写给人看的，PHP 执行时会跳过。共三种：`//` 和 `#` 只管一行（单行注释），`/* */` 管一段（多行注释）。注释掉代码是调试和排查问题的基本手段。

**操作**

```php
<?php
// 双斜杠：单行注释
# 井号：也是单行注释
/* 斜杠星号：多行注释
   可以写好几行 */
echo "注释会被跳过";
// 运行结果：
// 注释会被跳过
```

> ⚠️ `/* */` 不能套娃（不能嵌套另一个 `/* */`）。渗透里常把一句话木马藏进图片或正常代码里，靠注释伪装。

### `echo` 输出内容（最常用）

**解析**　把内容输出到页面（浏览器里看到的东西）。可以一次输出多个值、用逗号分隔，PHP 会把它们**直接拼在一起**（不会自动加空格）。注意 `echo` 是**语言结构不是函数**，没有返回值，也不能当函数来调用。

**操作**

```php
<?php
echo "你好";
echo "A", "B", "C";
echo 1 + 2;
// 运行结果：
// 你好ABC3
```

### `print` 输出内容并返回 1

**解析**　和 `echo` 几乎一样，唯一区别是 `print` **有返回值**（永远是 `1`），所以它能当表达式用、出现在赋值号右边；`echo` 不行。日常能用 echo 就用 echo，print 返回值这个特性很少用得上。

**操作**

```php
<?php
print "Hello";
$r = print "World";
echo "|返回值=" . $r;
// 运行结果：
// HelloWorld|返回值=1
```

### `print_r 与 var_dump` 打印变量的类型和结构

**解析**　调试最常用的两个输出函数：`print_r()` 按层级把数组/对象的**结构**打得好看，`var_dump()` 额外带上**类型和长度**。它们只负责显示，返回值没有意义（print_r 第二个参数传 true 才会把结果当字符串返回）。

**操作**

```php
<?php
$a = ["x" => 1, "y" => [2, 3]];
print_r($a);
echo "\n";
var_dump($a);
// 运行结果：
// Array
// (
//     [x] => 1
//     [y] => Array
//         (
//             [0] => 2
//             [1] => 3
//         )
//
// )
//
// array(2) {
//   ["x"]=>
//   int(1)
//   ["y"]=>
//   array(2) {
//     [0]=>
//     int(2)
//     [1]=>
//     int(3)
//   }
// }
```

> ⚠️ `print_r` 第二参数传 `true` 时不打印、而是返回字符串：`$s = print_r($a, true);`。反过来漏掉这个 `true` 就会把调试信息直接打到页面上。

### `变量` 用美元符号开头存数据

**解析**　变量用 `$` 开头、后面跟名字，**不需要声明类型**，赋什么就是什么类型，同一变量还能中途换类型（弱类型）。变量名区分大小写、不能数字开头。用 `var_dump()` 能看到一个值的类型和内容。

**操作**

```php
<?php
$name = "小明";
$age = 18;
var_dump($age);
$name = 3.14;      // 弱类型：同一变量可以先存字符串再存小数
var_dump($name);
var_dump($Age ?? "未定义（大小写不同）");
// 运行结果：
// int(18)
// float(3.14)
// string(30) "未定义（大小写不同）"
```

> ⚠️ 变量名**区分大小写**（`$Age` 和 `$age` 是两个变量），也不能数字开头。

### `常量` 定义后不能改的值

**解析**　常量定义后不能修改，使用时**不带 `$`**。两种写法：`define("名字", 值)` 和 `const 名字 = 值`。习惯上常量名全大写。PHP 还内置了一批常量，比如 `PHP_VERSION`（当前 PHP 版本）、`PHP_OS`。

**操作**

```php
<?php
define("SITE", "MyBlog");
const VERSION = "1.0";
echo SITE . "\n";
echo VERSION . "\n";
echo PHP_VERSION . "\n";
echo PHP_OS . "\n";
// 运行结果：
// MyBlog
// 1.0
// 8.5.11
// Darwin
```

> ⚠️ `const` 只能写在最外层（函数/循环里不行），`define()` 可以写在任何地方。给常量重新赋值会报错，这正是它比变量安全的地方。

### `heredoc 与 nowdoc` 多行字符串的两种写法

**解析**　要写很长、带换行的文本时，用 `<<<` 开头的 heredoc 最省事：它像双引号，里面的变量会被替换。`<<<'EOT'`（标识符加单引号）是 nowdoc，像单引号，内容原样保留。结束标识符必须**顶格、单独一行、后面跟分号**。

**操作**

```php
<?php
$name = "小明";
$h = <<<EOT
你好 $name
第二行
EOT;
$n = <<<'EOT'
你好 $name 不替换
EOT;
echo $h . "\n";
echo $n . "\n";
// 运行结果：
// 你好 小明
// 第二行
// 你好 $name 不替换
```

### `类型声明与严格模式` 给参数和返回值标类型

**解析**　函数参数和返回值前面都能写类型（`int`、`string`、`array`…）。默认是"弱模式"，传 `"3"` 会自动转成 `3`；在文件**第一行**写 `declare(strict_types=1);` 进入严格模式后类型不匹配直接抛 `TypeError`。给函数标类型能早发现错误，也是现代 PHP 的常规写法。

**操作**

```php
<?php
declare(strict_types=1);
function add(int $a, int $b): int {
    return $a + $b;
}
echo add(2, 3) . "\n";
try {
    echo add(2, "3");       // 严格模式下字符串 "3" 不接受
} catch (\TypeError $e) {
    echo "TypeError: " . $e->getMessage() . "\n";
}
// 运行结果：
// 5
// TypeError: add(): Argument #2 ($b) must be of type int, string given, called in /Users/zhangzixin/.hermes/cache/scratch/phpnote/run/snip.php on line 8
```

> ⚠️ `declare(strict_types=1);` 必须是**文件的第一条语句**，前面连空行/注释之外的东西都不能有，而且只影响本文件。

### `魔术常量` 随位置自动变化的预定义常量

**解析**　魔术常量会用双下划线包住、前后各两个，值取决于它**写在哪儿**：`__LINE__` 当前行号、`__FILE__` 当前文件完整路径、`__DIR__` 当前目录、`__FUNCTION__` 所在函数名、`__CLASS__` 所在类名。写日志、调试和自动加载时会用到。

**操作**

```php
<?php
function show() {
    echo __FUNCTION__ . "\n";   // 函数名
    echo __LINE__ . "\n";       // 当前行号
}
show();
echo basename(__FILE__) . "\n";
echo basename(__DIR__) . "\n";
echo PHP_VERSION . "\n";
// 运行结果：
// show
// 4
// snip.php
// run
// 8.5.11
```

> ⚠️ `__DIR__` 里的路径是**运行时的绝对路径**（本机跑出来就是本机路径），写死会换台机器就失效，通常配合 `__DIR__ . '/子目录'` 拼。

## 二 数据类型与运算符

### `字符串` 单引号与双引号的区别

**解析**　单引号里的内容**原样输出**：变量不替换、`\n` 也不换行。双引号会**解释变量**并把 `\n`（换行）、`\t`（制表）等转义字符变成真字符。想输出 `$` 本身、或不想让变量被替换，用单引号最省事。

**操作**

```php
<?php
$name = "小明";
echo '单引号：$name 不替换' . "\n";
echo "双引号：$name 会替换" . "\n";
echo '单引号 \n 不换行' . "\n";
echo "双引号 \n 会换行";
// 运行结果：
// 单引号：$name 不替换
// 双引号：小明 会替换
// 单引号 \n 不换行
// 双引号 
//  会换行
```

### `字符串拼接` 用点号连接

**解析**　PHP 用 `.`（点号）拼接字符串，**不是 `+`**。`.=` 是把右边追加到左边，等价于 `$a = $a . 右边`。数字和字符串用 `.` 拼时，数字自动转成字符串。

**操作**

```php
<?php
$a = "Hello";
$b = "PHP";
echo $a . " " . $b . "\n";
$s = $a;
$s .= " " . $b;
echo $s . "\n";
echo $a . 123 . "\n";
echo "1" . 2 . "\n";
// 运行结果：
// Hello PHP
// Hello PHP
// Hello123
// 12
```

> ⚠️ 别用 `+` 拼字符串：`echo "1" + 2;` 输出 `3`（当数字加），`echo "1" . 2;` 才是 `12`。而 `"abc" + 1` 在 PHP 8 里直接抛 `TypeError`（PHP 7 只是警告并返回 1）。

### `数据类型` 八种类型速览

**解析**　常打交道的类型：`int` 整数、`float` 小数、`string` 字符串、`bool` 布尔（`true`/`false`）、`array` 数组、`object` 对象、`null` 空值，加上少用的 `resource` 资源，一共八种。`var_dump()` 同时看类型和内容，`gettype()` 只返回类型名。

**操作**

```php
<?php
var_dump(1);
var_dump(1.5);
var_dump("abc");
var_dump(true);
var_dump(null);
var_dump([1, 2]);
// 运行结果：
// int(1)
// float(1.5)
// string(3) "abc"
// bool(true)
// NULL
// array(2) {
//   [0]=>
//   int(1)
//   [1]=>
//   int(2)
// }
```

### `类型转换` 显式与隐式转换

**解析**　在值前面加括号就能强制转换：`(int)`、`(float)`、`(string)`、`(bool)`、`(array)`。很多函数会自动转换（隐式）。转整数时**只取开头能识别的数字**，后面的字符丢掉、不报错。

**操作**

```php
<?php
var_dump((int)"12abc");
var_dump((int)"abc");
var_dump((float)"3.14");
var_dump((string)123);
var_dump((bool)"");
var_dump((bool)"0");
// 运行结果：
// int(12)
// int(0)
// float(3.14)
// string(3) "123"
// bool(false)
// bool(false)
```

> ⚠️ `(int)"12abc"` 得 `12`、`(int)"abc"` 得 `0`，都不报错——所以**判断是不是数字要用 `is_numeric($v)`**，不能靠强转。`(bool)""` 和 `(bool)"0"` 都是 false，这是 `""`/`"0"` 容易踩的坑。

### `类型判断函数` 用 is_ 系列判断类型

**解析**　`is_int` / `is_float` / `is_string` / `is_bool` / `is_array` / `is_object` / `is_null` 判断变量是不是某类型，返回 bool。`is_numeric()` 判断"能否当数字用"（`"12.3"` 为 true，`"12abc"` 为 false），比强转靠谱。

**操作**

```php
<?php
var_dump(is_int(5));
var_dump(is_string("x"));
var_dump(is_numeric("12.3"));
var_dump(is_numeric("12abc"));
var_dump(is_array([1]));
var_dump(is_null(null));
// 运行结果：
// bool(true)
// bool(true)
// bool(true)
// bool(false)
// bool(true)
// bool(true)
```

### `==与===` 弱比较与严格比较🔒

**解析**　`==` 只比较"值"，比较前会**先把两边转成同类型**，所以类型不同也可能判为相等；`===` 既比值也比类型，更严格。安全用途：判断用户输入、token、密码时用 `==` 会碰到"类型混淆""0e 魔法哈希"等绕过，**认证判断一律用 `===`**（或 `hash_equals()`）。

**操作**

```php
<?php
var_dump(1 == "1");
var_dump(1 === "1");
var_dump("0e1" == "0e2");
var_dump("abc" == 0);
var_dump(in_array(0, ["a", "b"]));
var_dump("100" == "1e2");
var_dump("" == 0);
// 运行结果：
// bool(true)
// bool(false)
// bool(true)
// bool(false)
// bool(false)
// bool(true)
// bool(false)
```

> ⚠️ 老文章里 `"abc" == 0`、`"" == 0`、`in_array(0, [...])` 这些绕过**在 PHP 8.0 已失效**（现在是 false）；但 `"0e1" == "0e2"` **依然为 true**。所以密码/签名比对绝不能写 `==`，要用 `===` 或 `hash_equals($known, $user)`。

### `算术运算符` 加减乘除取余

**解析**　`+` `-` `*` `/` 是加减乘除，`%` 取余，`**` 乘方。除法 `/` **总是返回浮点**（`7/2` 是 `3.5`），要整除用 `intdiv()`。取余结果符号跟被除数走。

**操作**

```php
<?php
echo 7 + 3 . "\n";
echo 7 / 2 . "\n";
echo intdiv(7, 2) . "\n";
echo 7 % 3 . "\n";
echo 2 ** 10 . "\n";
echo -7 % 3 . "\n";
// 运行结果：
// 10
// 3.5
// 3
// 1
// 1024
// -1
```

### `赋值与自增自减` 复合赋值与自增自减

**解析**　`+=` `-=` `*=` `.=` 等复合赋值是"运算后再存回自己"。`++` / `--` 在**前面**（`++$i`）先加再返回，在**后面**（`$i++`）先返回再加——这是很多笔试题的坑。

**操作**

```php
<?php
$x = 5;
$x += 3;  echo $x . "\n";
$x -= 2;  echo $x . "\n";
$x *= 2;  echo $x . "\n";
$i = 1;
echo $i++ . "\n";   // 先返回 1，再加到 2
echo $i . "\n";
echo ++$i . "\n";   // 先加到 3，再返回
// 运行结果：
// 8
// 6
// 12
// 1
// 2
// 3
```

### `逻辑运算符` 与或非的短路求值

**解析**　`&&`（与）、`||`（或）、`!`（非）。关键特性是**短路**：`&&` 左边为假时右边不执行，`||` 左边为真时右边不执行。利用短路可以把"先判断再执行"写得紧凑。`and`/`or` 也能用但优先级很低，一般不用。

**操作**

```php
<?php
function danger() { echo "被调用了！"; return true; }
var_dump(true && false);
var_dump(true || false);
var_dump(!true);
var_dump(false && danger());   // 短路：danger() 不执行
var_dump(true || danger());    // 短路：danger() 也不执行
// 运行结果：
// bool(false)
// bool(true)
// bool(false)
// bool(false)
// bool(true)
```

### `位运算符` 按位运算

**解析**　对整数的二进制逐位操作：`&` 与、`|` 或、`^` 异或、`~` 取反、`<<` 左移、`>>` 右移。日常业务少用，但**权限位、标志位、编码解码**和 CTF 里很常见。

**操作**

```php
<?php
echo (6 & 3) . "\n";    // 110 & 011 = 010
echo (6 | 3) . "\n";    // 110 | 011 = 111
echo (6 ^ 3) . "\n";    // 110 ^ 011 = 101
echo (~6) . "\n";       // 按位取反
echo (1 << 3) . "\n";   // 左移 3 位
echo (16 >> 2) . "\n";  // 右移 2 位
// 运行结果：
// 2
// 7
// 5
// -7
// 8
// 4
```

### `null 与 isset、empty` 判断变量是否设置或为空🔒

**解析**　`isset($v)` 变量存在且不为 null 时为 true；`empty($v)` 变量"为空"时为 true——`""`、`0`、`"0"`、`null`、`false`、空数组都算空。两个函数对**未定义的变量都不报警告**，所以常用于安全地取参数。判断用户到底传没传值，用 `isset`；判断值是否有效，用 `empty`。

**操作**

```php
<?php
$a = null;
var_dump(isset($a));
var_dump(empty($a));
$b = "";
var_dump(isset($b));
var_dump(empty($b));
$c = "0";
var_dump(empty($c));
var_dump(isset($undefined));
// 运行结果：
// bool(false)
// bool(true)
// bool(true)
// bool(true)
// bool(true)
// bool(false)
```

> ⚠️ `empty("0")` 是 true，而 `"0"` 往往是合法输入（比如数量 0、验证码 0），**别拿 empty 判断"有没有填"**。安全提示：判断登录用户等场景优先 `isset`+`!== null`，避免 `"0"` 被当成没值。

## 三 字符串与正则

### `常用字符串函数` 长度、大小写、截取与替换

**解析**　`strlen()` 长度，`strtolower()`/`strtoupper()` 大小写，`str_replace(找, 换, 原串)` 替换，`substr(串, 起, 长)` 截取（负数表示从末尾数），`strpos()` 找首次出现的位置（**找不到返回 false**），`trim()` 去首尾空白，`str_contains()` 判断包含（PHP 8+）。

**操作**

```php
<?php
$s = "Hello World";
echo strlen($s) . "\n";
echo strtolower($s) . "\n";
echo strtoupper($s) . "\n";
echo str_replace("World", "PHP", $s) . "\n";
echo substr($s, 0, 5) . "\n";
echo strpos($s, "World") . "\n";
echo "[" . trim("  a,b  ") . "]" . "\n";
var_dump(str_contains($s, "World"));
// 运行结果：
// 11
// hello world
// HELLO WORLD
// Hello PHP
// Hello
// 6
// [a,b]
// bool(true)
```

> ⚠️ `strlen()` 数的是**字节**，一个汉字占 3 字节（`strlen("小明")` 是 6），要按字数算用 `mb_strlen("小明")`（得 2）。`strpos` 找不到返回 `false`，而位置可能是 `0`，所以判断要用 `!== false`，不能写 `== false`（见第 4 章 in_array 的同类坑）。

### `mb_ 系列函数` 正确按字数处理中文

**解析**　`strlen`/`substr` 按字节处理，中文会乱。加 `mb_` 前缀的版本按**字符**处理：`mb_strlen` 数个数、`mb_substr` 按字截取、`mb_strtoupper` 处理多字节大小写。项目里凡是可能含非 ASCII 的字符串都该用 `mb_` 版。

**操作**

```php
<?php
$s = "小明ABC";
echo strlen($s) . "\n";       // 字节数
echo mb_strlen($s) . "\n";    // 字符数
echo mb_substr($s, 0, 2) . "\n";
echo mb_strtoupper("abc") . "\n";
// 运行结果：
// 9
// 5
// 小明
// ABC
```

> ⚠️ 用 `mb_substr` 按字节截断中文会切出半个字，产生乱码（`�`）。`mb_*` 函数在部分环境要额外开扩展，用前可 `function_exists('mb_strlen')` 检查。

### `sprintf` 格式化字符串

**解析**　`sprintf(格式, 参数...)` 把值按格式**拼成字符串返回**（不直接输出），`printf` 则直接输出。常用占位：`%s` 字符串、`%d` 整数、`%f` 浮点（`%.2f` 保留两位）、`%x` 十六进制、`%05d` 补零。这是日志、拼 SQL、拼 URL 的常用工具。

**操作**

```php
<?php
$name = "小明";
$n = 7;
echo sprintf("你好 %s，你有 %d 条消息\n", $name, $n);
printf("%.2f\n", 3.14159);
printf("%05d\n", 42);
printf("%x\n", 255);
printf("%s|%10s|%-10s|\n", "a", "b", "c");
// 运行结果：
// 你好 小明，你有 7 条消息
// 3.14
// 00042
// ff
// a|         b|c         |
```

### `str_pad、str_repeat、strrev` 补位、重复与反转

**解析**　`str_pad(串, 总长度, 填充串, 方向)` 把字符串补到指定长度（默认右补，`STR_PAD_LEFT` 左补），生成编号、对齐很常用。`str_repeat(串, 次数)` 重复，`strrev(串)` 反转。

**操作**

```php
<?php
echo str_pad("7", 3, "0", STR_PAD_LEFT) . "\n";
echo str_pad("ab", 5, "-") . "\n";
echo str_repeat("=", 5) . "\n";
echo strrev("abc") . "\n";
// 运行结果：
// 007
// ab---
// =====
// cba
```

### `explode 与 implode` 字符串与数组互转

**解析**　`explode(分隔符, 字符串)` 把字符串切成数组，`implode(分隔符, 数组)` 把数组拼成字符串。CSV、CSV 行、URL 参数这类"一个字符串装多条数据"的格式，都靠它们进出数组。

**操作**

```php
<?php
$arr = explode(",", "a,b,c");
print_r($arr);
echo implode(" | ", $arr) . "\n";
echo implode(",", [1, 2, 3]) . "\n";
echo count(explode(",", "x,y,z,w")) . "\n";
// 运行结果：
// Array
// (
//     [0] => a
//     [1] => b
//     [2] => c
// )
// a | b | c
// 1,2,3
// 4
```

### `preg_match` 正则单次匹配🔒

**解析**　`preg_match(模式, 字符串, $匹配结果)` 只要匹配到一次就返回 `1`，否则 `0`（出错返回 false）。第三个参数自动被填成一个数组：`$m[0]` 是整个匹配到的内容，`$m[1]`、`$m[2]`……是各括号分组的内容。模式要写成 `"/.../"` 带定界符。

**操作**

```php
<?php
preg_match("/\d+/", "电话 13800138000", $m);
print_r($m);
preg_match("/(\d{4})-(\d{2})-(\d{2})/", "日期 2026-10-08", $d);
print_r($d);
var_dump(preg_match("/^admin$/", "admin"));
// 运行结果：
// Array
// (
//     [0] => 13800138000
// )
// Array
// (
//     [0] => 2026-10-08
//     [1] => 2026
//     [2] => 10
//     [3] => 08
// )
// int(1)
```

> ⚠️ 匹配失败时第三个参数里的 `$m` 是**空数组**，直接读 `$m[1]` 会报 `Undefined array key`。用 `if (preg_match(...))` 包一层再取分组。

### `preg_match_all` 正则全部匹配🔒

**解析**　`preg_match_all` 把字符串里**所有**匹配都找出来，返回匹配到的总数，结果放进第三个参数：`$m[0]` 是所有完整匹配组成的数组，`$m[1]` 是第一个分组的所有内容。做数据提取、爬虫清洗很常用。

**操作**

```php
<?php
preg_match_all("/\d+/", "a1b22c333", $m);
print_r($m[0]);
echo "匹配数：" . count($m[0]) . "\n";
preg_match_all("/(\w+)@(\w+)/", "a@x b@y", $e);
print_r($e[1]);
// 运行结果：
// Array
// (
//     [0] => 1
//     [1] => 22
//     [2] => 333
// )
// 匹配数：3
// Array
// (
//     [0] => a
//     [1] => b
// )
```

### `preg_replace` 正则查找替换🔒

**解析**　`preg_replace(模式, 替换, 原串)` 把匹配到的部分换成新内容、返回新字符串。替换串里可用 `$1`、`$2` 引用分组内容。**这是过滤/白名单/清洗输入的主力**，但用错正则等于没防。

**操作**

```php
<?php
echo preg_replace("/\s+/", "_", "a  b   c") . "\n";
echo preg_replace("/[0-9]+/", "#", "a1b22") . "\n";
echo preg_replace("/(\w+)@(\w+)/", "$2#$1", "admin@site") . "\n";
// 运行结果：
// a_b_c
// a#b#
// site#admin
```

> ⚠️ `preg_replace` 曾有一个 `/e` 修饰符（把替换结果当代码执行），**PHP 7 起已删除**，老站点的 `/e` 会直接报错。看到 `preg_replace(.../e)` 说明这是很老的代码。

### `正则元字符` 常用元字符与修饰符速查

**解析**　元字符：`.` 任意字符、`\d` 数字、`\w` 字母数字下划线、`\s` 空白、`*` 0 次以上、`+` 1 次以上、`?` 0 或 1 次、`{n}` 恰好 n 次、`^` 开头、`$` 结尾、`[]` 字符集、`()` 分组、`\b` 词边界。修饰符放在定界符后面：`i` 忽略大小写、`m` 多行、`s` 让 `.` 匹配换行、`u` 按 UTF-8 处理。

**操作**

```php
<?php
var_dump(preg_match("/^abc$/i", "ABC"));
var_dump(preg_match("/\w+/", "hi_there"));
var_dump(preg_match("/colou?r/", "color"));
var_dump(preg_match("/\bfox\b/", "a fox!"));
var_dump(preg_match("/[0-9]{3}/", "12 345"));
// 运行结果：
// int(1)
// int(1)
// int(1)
// int(1)
// int(1)
```

> ⚠️ 正则不加 `u` 修饰符时按字节匹配，处理中文会出问题；过滤中文/UTF-8 输入要写 `"/.../u"`。另外 `^`/`$` 默认只匹配整个字符串的首尾，要多行匹配得加 `m`。

## 四 数组与常用函数

### `数组` 索引数组

**解析**　数组存一组值，用 `[]` 定义，下标**从 0 开始**。`$arr[下标]` 取值，`$arr[] = 值` 在末尾追加，`count($arr)` 数元素个数。老写法 `array(1,2,3)` 和 `[1,2,3]` 完全等价。

**操作**

```php
<?php
$fruits = ["apple", "banana", "cherry"];
echo $fruits[0] . "\n";
echo count($fruits) . "\n";
$fruits[] = "date";
echo $fruits[3] . "\n";
$arr = array(1, 2, 3);       // 老写法，等价
echo $arr[2] . "\n";
// 运行结果：
// apple
// 3
// date
// 3
```

### `关联数组` 键值对

**解析**　关联数组用 `键 => 值` 存数据（像一本小字典），取值写 `$arr["键"]`。`print_r()` 能把整个数组按层级打印出来看结构，`var_dump()` 还会带上类型和长度。PHP 的数组是**有序的**，插入顺序就是遍历顺序。

**操作**

```php
<?php
$user = ["name" => "小明", "age" => 18];
echo $user["name"] . "\n";
$user["age"] = 19;
$user["city"] = "北京";
print_r($user);
// 运行结果：
// 小明
// Array
// (
//     [name] => 小明
//     [age] => 19
//     [city] => 北京
// )
```

### `多维数组` 嵌套数组

**解析**　数组里可以再装数组，形成多维结构——查表、装一批记录都用它。访问写成 `$arr[外层键][内层键]`，`count()` 只数**最外层**元素个数。

**操作**

```php
<?php
$users = [
    ["name" => "admin", "age" => 30],
    ["name" => "alice", "age" => 25],
];
echo $users[0]["name"] . "\n";
echo $users[1]["age"] . "\n";
echo count($users) . "\n";
// 运行结果：
// admin
// 25
// 2
```

### `foreach 遍历` 遍历数组

**解析**　`foreach` 专门用来遍历数组：`foreach ($arr as $v)` 只拿每个值；`foreach ($arr as $k => $v)` 同时拿到键和值。比用 for 加下标省事，关联数组也能直接遍历。想做"值修改回原数组"，用 `foreach ($arr as &$v)`。

**操作**

```php
<?php
$fruits = ["apple", "banana"];
foreach ($fruits as $v) {
    echo $v . "\n";
}
$user = ["name" => "小明", "age" => 18];
foreach ($user as $k => $v) {
    echo "$k = $v\n";
}
// 运行结果：
// apple
// banana
// name = 小明
// age = 18
```

> ⚠️ 引用遍历 `foreach ($arr as &$v)` 循环结束后**必须 `unset($v);`**，否则后面再用 `$v` 会莫名改到数组最后一个元素（引用还挂着）。

### `常用数组函数` 计数、增删与查找

**解析**　`count()` 数个数，`array_push()` 末尾追加、`array_pop()` 弹出末尾，`array_unshift()`/`array_shift()` 在开头增删，`array_sum()` 求和，`array_key_exists()` 判断键在不在。

**操作**

```php
<?php
$a = [3, 1, 2];
echo count($a) . "\n";
array_push($a, 9);
echo implode(",", $a) . "\n";
$last = array_pop($a);
echo $last . "\n";
echo array_sum($a) . "\n";
var_dump(array_key_exists(0, $a));
// 运行结果：
// 3
// 3,1,2,9
// 9
// 6
// bool(true)
```

### `排序函数` sort、asort、ksort、usort

**解析**　`sort` 按值升序并**重排下标**；`asort` 按值排序但**保留键**（关联数组常用）；`ksort` 按键排序；`usort` 用自己写的回调决定顺序。降序用 `rsort`/`arsort`/`krsort`。它们都是**原地修改**，直接改变传入的数组、返回 bool。

**操作**

```php
<?php
$nums = [3, 1, 2];
sort($nums);
echo "sort: " . implode(",", $nums) . "\n";
$ages = ["bob" => 30, "amy" => 25];
asort($ages);
print_r($ages);
$keys = ["b" => 1, "a" => 2];
ksort($keys);
print_r($keys);
$n = [3, 1, 2];
usort($n, fn($x, $y) => $y <=> $x);   // 降序
echo "usort降序: " . implode(",", $n) . "\n";
// 运行结果：
// sort: 1,2,3
// Array
// (
//     [amy] => 25
//     [bob] => 30
// )
// Array
// (
//     [a] => 2
//     [b] => 1
// )
// usort降序: 3,2,1
```

> ⚠️ `sort` 会把键重置成 0,1,2，关联数组用它会**丢掉键名**——要保键用 `asort`/`ksort`。另外这些函数原地排序，别指望它返回排好的数组（返回的是 true/false）。

### `array_map、array_filter、array_reduce` 用回调处理数组

**解析**　`array_map(fn, $arr)` 对每个元素做同样变换、返回新数组；`array_filter($arr, fn)` 留下回调为真的元素（**保留原来的键**）；`array_reduce($arr, fn, $初始)` 把数组归并成一个值。这三个是函数式处理数组的主力。

**操作**

```php
<?php
$a = [1, 2, 3, 4];
print_r(array_map(fn($x) => $x * 2, $a));
print_r(array_filter($a, fn($x) => $x % 2 === 0));
echo array_reduce($a, fn($carry, $x) => $carry + $x, 0) . "\n";
// 运行结果：
// Array
// (
//     [0] => 2
//     [1] => 4
//     [2] => 6
//     [3] => 8
// )
// Array
// (
//     [1] => 2
//     [3] => 4
// )
// 10
```

> ⚠️ `array_filter` **保留原键**，过滤后下标可能不连续（如 `[1,3]`），要重排用 `array_values(array_filter(...))`。只传数组不传回调时，它会删掉所有"假值"（`0`、`""`、`null`、`false`），常被误用。

### `array_merge` 合并数组的两种区别

**解析**　`array_merge($a, $b)` 把两个数组合并，**字符串键后者覆盖前者、数字键则重排追加**；`$a + $b` 是**并集**，键冲突时保留左边、右边被忽略。想"后者覆盖"用 merge，想"缺的才补"用 `+`。

**操作**

```php
<?php
$a = ["x" => 1, "y" => 2];
$b = ["y" => 9, "z" => 3];
print_r(array_merge($a, $b));
print_r($a + $b);
// 运行结果：
// Array
// (
//     [x] => 1
//     [y] => 9
//     [z] => 3
// )
// Array
// (
//     [x] => 1
//     [y] => 2
//     [z] => 3
// )
```

### `array_column、array_keys、array_values` 取列与取键值

**解析**　`array_column($arr, "字段")` 从一堆记录里抽出某一列（做下拉、ID 列表很方便）；`array_keys()` 取所有键，`array_values()` 取所有值（可把关联数组转成索引数组）。

**操作**

```php
<?php
$users = [
    ["id" => 1, "name" => "admin"],
    ["id" => 2, "name" => "alice"],
];
print_r(array_column($users, "name"));
print_r(array_keys($users[0]));
print_r(array_values(["a" => 1, "b" => 2]));
// 运行结果：
// Array
// (
//     [0] => admin
//     [1] => alice
// )
// Array
// (
//     [0] => id
//     [1] => name
// )
// Array
// (
//     [0] => 1
//     [1] => 2
// )
```

> ⚠️ `array_column` 是 **PHP 5.5+** 才有；老环境没有就老老实实用 foreach 抽列。

### `in_array 与 array_search` 查找元素是否存在🔒

**解析**　`in_array($值, $数组)` 判断值在不在数组里，返回 bool；`array_search($值, $数组)` 返回**找到的键**，找不到返回 `false`。安全用途：做"白名单"时若用默认弱比较，`in_array(0, ["a","b"])`、`in_array("1", [1,2])` 这类绕过就会放行。

**操作**

```php
<?php
$a = [1, 2, 3];
var_dump(in_array(2, $a));
var_dump(in_array("2", $a));         // 弱比较：字符串 "2" 也 true
var_dump(in_array("2", $a, true));   // 严格：类型不同 → false
var_dump(array_search(3, $a));       // 键
var_dump(array_search("9", $a));     // 找不到 → false
// 运行结果：
// bool(true)
// bool(true)
// bool(false)
// int(2)
// bool(false)
```

> ⚠️ 白名单校验**必须传第三个参数 `true`** 走严格比较：`in_array($v, $allow, true)`。`array_search` 找不到返回 `false`，而合法键可能是 `0`，判断要用 `!== false`。

### `array_slice 与 array_splice` 截取与移除替换

**解析**　`array_slice($arr, 起, 长)` **复制**一段出来、原数组不变；`array_splice($arr, 起, 长, [替换])` 会**直接改动原数组**——把一段切掉（可选插入新元素），并返回被切掉的部分。名字差一个 `p`，行为差很多。

**操作**

```php
<?php
$a = [1, 2, 3, 4, 5];
print_r(array_slice($a, 1, 2));
$b = $a;
print_r(array_splice($b, 1, 2, [99]));
print_r($b);
// 运行结果：
// Array
// (
//     [0] => 2
//     [1] => 3
// )
// Array
// (
//     [0] => 2
//     [1] => 3
// )
// Array
// (
//     [0] => 1
//     [1] => 99
//     [2] => 4
//     [3] => 5
// )
```

> ⚠️ `array_slice` 不改原数组、`array_splice` 改原数组——记混了会莫名其妙丢数据。

### `list 与数组解构` 解构赋值

**解析**　把数组里的值一次赋给多个变量：`[$a, $b] = [1, 2]`（老写法 `list($a, $b) = ...`）。关联数组也能解：`["x" => $x] = $arr`。位置想跳过就用空位 `[, $b]`。处理函数返回的 `[$code, $msg]` 这类多值结果特别顺手。

**操作**

```php
<?php
[$a, $b] = [1, 2];
echo "$a $b\n";
["x" => $x, "y" => $y] = ["x" => 10, "y" => 20];
echo "$x $y\n";
[, $second] = ["跳过", "保留"];
echo $second . "\n";
// 运行结果：
// 1 2
// 10 20
// 保留
```

## 五 流程控制

### `if、else if、else` 条件分支

**解析**　按条件选择执行哪段：条件为真执行 `if` 里的，否则看 `elseif`，全不满足执行 `else`。`else if` 和 `elseif` 两种写法都行。条件为真后**其余分支不再判断**。

**操作**

```php
<?php
$score = 85;
if ($score >= 90) {
    echo "优秀";
} elseif ($score >= 60) {
    echo "及格";
} else {
    echo "不及格";
}
echo "\n";
// 运行结果：
// 及格
```

> ⚠️ 判断相等别少写一个等号：一个 `=` 是赋值（会真改值），比较用 `==` 或 `===`。

### `switch、case` 多路分支🔒

**解析**　一个变量要和多个固定值比较时，`switch` 比一串 `if-elseif` 更清楚：匹配到哪个 `case` 就执行哪段。注意 `switch` 用的是**松散比较**（`==`）。都不匹配执行 `default`。

**操作**

```php
<?php
$day = 3;
switch ($day) {
    case 1:
        echo "周一";
        break;
    case 3:
        echo "周三";
        break;
    default:
        echo "其他";
}
echo "\n";
// 运行结果：
// 周三
```

> ⚠️ 每个 `case` 末尾记得 `break`，否则会"穿透"（fall-through）继续执行下一个 case 的代码。`switch` 用松散比较，`case "abc"` 在某些值下可能被 `== 0` 命中——安全敏感的匹配改用 `match`（严格）或 if+`===`。

### `match 表达式` 值匹配并返回（PHP 8）

**解析**　`match`（PHP 8 新增）像 switch 的表达式版：匹配到就**返回对应值**，可以直接赋给变量。它是**严格比较**（`===`），没有匹配又没写 `default` 会抛 `UnhandledMatchError`。多个条件可用逗号并列。

**操作**

```php
<?php
$status = 2;
echo match ($status) {
    1, 2 => "进行中",
    3 => "已完成",
    default => "未知",
} . "\n";
$v = match (true) {
    $status > 5 => "大",
    default => "小",
};
echo $v . "\n";
// 运行结果：
// 进行中
// 小
```

> ⚠️ `match` 用严格比较且**每个分支只能是一个表达式**，不支持像 switch 那样塞多行语句；要写复杂逻辑就把 match 结果再拿去用。忘写 `default` 且没匹配上会抛异常。

### `for 循环` 已知次数的循环

**解析**　`for (初始化; 条件; 步进) { ... }`，循环次数确定时用它。三段用分号隔开，条件为假就停。三段都可以省，但要小心死循环。

**操作**

```php
<?php
for ($i = 0; $i < 3; $i++) {
    echo $i . " ";
}
echo "\n";
for ($i = 5; $i > 0; $i -= 2) {
    echo $i . " ";
}
echo "\n";
// 运行结果：
// 0 1 2 
// 5 3 1 
```

### `while、do-while` 条件循环

**解析**　`while (条件)` 条件为真就一直循环；`do { ... } while (条件)` **先执行一次再判断**，所以循环体至少执行一次（即使一开始条件就是假）。循环次数不确定时用它。

**操作**

```php
<?php
$i = 0;
while ($i < 3) {
    echo $i;
    $i++;
}
echo "\n";
$j = 5;
do {
    echo $j;
    $j++;
} while ($j < 3);
echo "\n";
// 运行结果：
// 012
// 5
```

> ⚠️ `while` 里忘了改条件变量会死循环，把服务器 CPU 跑满。写循环先想清楚"什么时候退出"。

### `break 与 continue` 跳出与跳过

**解析**　`break` 结束**整个循环**；`continue` 只跳过**本次**剩余代码、直接进入下一次。多层循环里在它们后面加个数字 `break 2;` / `continue 2;` 表示跳出/继续外层第几层。

**操作**

```php
<?php
for ($i = 1; $i <= 5; $i++) {
    if ($i == 3) continue;
    if ($i == 5) break;
    echo $i;
}
echo "\n";
foreach ([1, 2, 3] as $v) {
    foreach (["a", "b"] as $w) {
        if ($w === "b") continue 2;   // 跳到外层下一次
        echo "$v$w ";
    }
}
echo "\n";
// 运行结果：
// 124
// 1a 2a 3a 
```

### `三元运算符与空合并` 一行判断与给默认值

**解析**　`条件 ? 真值 : 假值` 是一行版 if-else；`$a ?: $b` 是"左边为真就用左边，否则用右边"；`$a ?? $b` 是"左边存在且不为 null 就用左边，否则用右边"——专门给没传的参数兜底。`??=` 是"为空就赋值"。

**操作**

```php
<?php
$age = 18;
echo $age >= 18 ? "成年" : "未成年";
echo "\n";
echo ($_GET["name"] ?? "游客") . "\n";
echo ($undefined ?? "默认值") . "\n";
echo (($_GET["p"] ?? null) ?: "空或假") . "\n";
// 运行结果：
// 成年
// 游客
// 默认值
// 空或假
```

> ⚠️ `??` 对**未定义的变量也不报警告**，是安全取参数的标准写法；而 `?:` 碰到未定义变量会报 `Undefined variable`。`??` 只在"null/不存在"时兜底，空字符串 `""` 不会触发兜底——要用 `?:` 才行。

### `替代语法` 模板里的 if 和 for 写法

**解析**　把 `{ }` 换成 `:` 加 `endif;` / `endforeach;` / `endfor;`，是 PHP 模板的经典写法（WordPress 主题里到处都是）。它让 HTML 和 PHP 混排更清楚。`<?= $v ?>` 是 `<?php echo $v; ?>` 的简写。

**操作**

```php
<?php $items = ["苹果", "香蕉"]; ?>
<ul>
<?php foreach ($items as $it): ?>
    <li><?= $it ?></li>
<?php endforeach; ?>
</ul>
<?php if (count($items) > 1): ?>
共 <?= count($items) ?> 项
<?php endif; ?>
// 运行结果：
// <ul>
//     <li>苹果</li>
//     <li>香蕉</li>
// </ul>
// 共 2 项
```

## 六 函数

### `函数定义与调用` 把逻辑打包复用

**解析**　用 `function 名字(参数) { ... }` 定义一段可复用的逻辑，`return` 把结果交回去，调用时写名字加括号。函数里的变量默认和外面互不影响（各自作用域）。

**操作**

```php
<?php
function sayHi($name) {
    return "你好，" . $name;
}
echo sayHi("小明") . "\n";
echo gettype(sayHi("PHP")) . "\n";
// 运行结果：
// 你好，小明
// string
```

### `函数参数与返回值` 默认值与引用传参

**解析**　参数可以带默认值（**必须放在参数列表最后**），不传就用默认。参数前加 `&` 是**引用传参**，函数内部改了它、外面的变量也跟着变。没写 `return` 时函数返回 `null`。

**操作**

```php
<?php
function greet($name, $greeting = "你好") {
    return "{$greeting}，{$name}";
}
echo greet("小明") . "\n";
echo greet("Tom", "Hi") . "\n";
function addOne(&$n) {
    $n++;
}
$x = 5;
addOne($x);
echo $x . "\n";
// 运行结果：
// 你好，小明
// Hi，Tom
// 6
```

> ⚠️ 双引号里**中文标点紧跟变量名会被当成变量名的一部分**：写 `"$greeting，$name"` 会报 `Undefined variable $greeting，`。正确写法是用 `{}` 划清边界（`"{$greeting}，{$name}"`）或用 `.` 拼接。

### `可变参数与参数解包` 收不定个数的参数

**解析**　参数写 `...$args` 表示"收下所有多余参数"，函数里 `$args` 是一个数组。反过来，调用时写 `f(...$arr)` 可以把数组"拆开"当成多个参数传进去。包装函数、日志、`max()` 这类都靠它。

**操作**

```php
<?php
function sum(...$nums) {
    return array_sum($nums);
}
echo sum(1, 2, 3, 4) . "\n";
$args = [10, 20, 30];
echo sum(...$args) . "\n";
// 运行结果：
// 10
// 60
```

### `匿名函数与闭包` 没有名字的函数

**解析**　匿名函数（闭包）是"没有名字的函数"，赋给变量或当参数传。想用它访问外部变量，必须在后面用 `use ($var)` 列出来（默认访问不到）。回调、排序、事件处理里到处是它。

**操作**

```php
<?php
$greet = function ($name) {
    return "你好，" . $name;
};
echo $greet("小明") . "\n";
$prefix = "【重要】";
$f = function ($msg) use ($prefix) {
    return $prefix . $msg;
};
echo $f("会议提醒") . "\n";
// 运行结果：
// 你好，小明
// 【重要】会议提醒
```

> ⚠️ `use ($var)` 默认是**按值捕获**（改不了外面），要按引用改写成 `use (&$var)`。PHP 里闭包靠它进作用域，这点和 JS 自动捕获不同。

### `箭头函数` 一行式闭包（PHP 7.4+）

**解析**　`fn(参数) => 表达式` 是一行版闭包，**自动捕获**外层变量（不用写 `use`），但函数体只能是一个表达式。短小的回调（`array_map`、`usort`）用它最清爽。

**操作**

```php
<?php
$double = fn($x) => $x * 2;
echo $double(5) . "\n";
print_r(array_map(fn($n) => $n * 10, [1, 2, 3]));
$factor = 3;
$scale = fn($x) => $x * $factor;   // 自动捕获 $factor
echo $scale(4) . "\n";
// 运行结果：
// 10
// Array
// (
//     [0] => 10
//     [1] => 20
//     [2] => 30
// )
// 12
```

### `变量作用域` 局部、全局与 static🔒

**解析**　函数内是**局部作用域**，外面的变量默认进不来。要用全局变量得声明 `global $g;` 或从 `$GLOBALS['g']` 取。函数里的 `static $x` 是"跨调用保留"的局部变量（只初始化一次）。

**操作**

```php
<?php
$g = "全局";
function show() {
    global $g;
    static $count = 0;
    $count++;
    return $count . "-" . $g;
}
echo show() . "\n";
echo show() . "\n";
echo $g . "\n";
// 运行结果：
// 1-全局
// 2-全局
// 全局
```

> ⚠️ 滥用 `global` 会让代码难维护，能用参数传就别用 global。渗透里 `global`/`$GLOBALS` 常被用于"变量覆盖"类漏洞（把内部变量改成攻击者的值）。

### `递归函数` 函数调用自己

**解析**　递归是函数直接或间接调用自己，必须有"出口"（终止条件），否则会无限递归直到栈溢出。阶乘、目录遍历、树结构处理都常用。

**操作**

```php
<?php
function factorial($n) {
    if ($n <= 1) return 1;          // 出口
    return $n * factorial($n - 1);
}
echo factorial(5) . "\n";
// 运行结果：
// 120
```

> ⚠️ 递归深度太大会报 `Maximum function nesting`（默认约 256 层）或耗尽内存，深目录/深树改用循环或迭代器。

### `变量函数与 call_user_func` 用字符串/变量调用函数🔒

**解析**　把函数名存进变量或字符串，就能**动态调用**：`$f = "system"; $f("id");`。`call_user_func($f, ...args)` 是它的函数版，常用于回调、路由分发。灵活，但也是危险入口。

**操作**

```php
<?php
function hello() { return "hello\n"; }
$fn = "hello";
echo $fn();
foreach (["strtoupper", "strtolower"] as $f) {
    echo call_user_func($f, "AbC") . "\n";
}
// 运行结果：
// hello
// ABC
// abc
```

> ⚠️ **渗透重点**：只要函数名来自用户输入（如 `$_GET['fn'](...)`），攻击者就能调用任意函数——配上 `"system"` 就是命令执行。路由、插件系统千万别让用户决定调什么函数。

## 七 面向对象

### `类与对象` 定义类并实例化

**解析**　`class 名字 { ... }` 定义类（模板），`new 类名()` 造出一个对象（实例）。类里的函数叫**方法**，用 `$this` 在方法内访问当前对象的属性/方法，外面用 `->` 调用。

**操作**

```php
<?php
class User {
    public $name;
    public function hello() {
        return "我是 " . $this->name;
    }
}
$u = new User();
$u->name = "小明";
echo $u->hello() . "\n";
// 运行结果：
// 我是 小明
```

### `类常量与属性` 类里的变量和固定值

**解析**　属性是对象自己的变量（用 `public $x` 声明），类常量是整类共享的固定值（`const NAME = 值`，**没有 `$`**）。常量用 `类名::常量名` 访问，不用 new 也能取。PHP 7.4+ 还支持给属性标类型，PHP 8 支持构造器里直接写 `public string $name`。

**操作**

```php
<?php
class Config {
    const VERSION = "1.0";
    public string $env = "dev";
}
echo Config::VERSION . "\n";
$c = new Config();
echo $c->env . "\n";
// 运行结果：
// 1.0
// dev
```

> ⚠️ 类常量不能用 `$this->` 访问，要写 `self::VERSION`（类内）或 `类名::VERSION`（类外）。

### `构造与析构函数` 创建与销毁对象时自动调用🔒

**解析**　`__construct()` 在 `new` 时自动执行，用来初始化属性/建连接；`__destruct()` 在对象被销毁（`unset` 或脚本结束时）自动执行，用来收尾/关连接。它们**都不能手动调用**。

**操作**

```php
<?php
class Person {
    public function __construct(public string $name) {
        echo "构造：{$this->name}\n";
    }
    public function __destruct() {
        echo "析构：{$this->name}\n";
    }
}
$p = new Person("小明");
echo "使用中\n";
unset($p);
echo "已销毁\n";
// 运行结果：
// 构造：小明
// 使用中
// 析构：小明
// 已销毁
```

> ⚠️ **反序列化漏洞的关键**：`unserialize()` 时 `__destruct`/`__wakeup` 会自动触发，攻击者构造恶意数据就能借这些魔术方法执行代码。审计反序列化时先找 `__destruct`/`__wakeup`。

### `继承` 用 extends 复用父类

**解析**　`class 子 extends 父` 让子类拥有父类的属性和方法，还可以**重写**（覆盖）它们。子类里用 `parent::方法()` 调父类版本。`instanceof` 判断一个对象是不是某类（或其子类）的实例。

**操作**

```php
<?php
class Animal {
    public function speak() {
        return "……";
    }
}
class Dog extends Animal {
    public function speak() {
        return parent::speak() . "汪汪";
    }
}
$d = new Dog();
echo $d->speak() . "\n";
var_dump($d instanceof Animal);
// 运行结果：
// ……汪汪
// bool(true)
```

### `访问控制` public、protected、private

**解析**　成员前的关键字决定谁能访问：`public` 哪都能访问；`protected` 只有本类和子类能访问；`private` 只有本类能访问。越私有越安全，业务里"能 private 就 private"。

**操作**

```php
<?php
class Account {
    public $owner = "公开";
    protected $balance = 100;
    private $pin = "1234";
    public function getBalance() {
        return $this->balance;      // 类内可访问 protected/private
    }
}
$a = new Account();
echo $a->owner . "\n";
echo $a->getBalance() . "\n";
// echo $a->balance;   // ❌ protected 不能在类外访问
// echo $a->pin;       // ❌ private 只有本类能访问
// 运行结果：
// 公开
// 100
```

### `静态成员` static 与 self、::

**解析**　`static` 属性和方法**属于类本身而非某个对象**，用 `类名::成员` 访问、不用 `new`。类内用 `self::` 指当前类、`parent::` 指父类、`static::` 是"后期静态绑定"。它们常用于工具函数、单例、计数器。

**操作**

```php
<?php
class Counter {
    public static int $count = 0;
    public static function inc() {
        self::$count++;
    }
}
Counter::inc();
Counter::inc();
echo Counter::$count . "\n";
// 运行结果：
// 2
```

> ⚠️ 静态方法里**没有 `$this`**，不能访问普通（非静态）属性。别为了省事把一切都写成 static——它会让代码难测试、共享状态容易出 bug。

### `抽象类与接口` abstract 与 interface

**解析**　抽象类（`abstract class`）不能直接 new，可以只声明方法名、逼子类实现，也能含已实现的方法；接口（`interface`）只声明"必须有哪些方法"，一个类用 `implements` 可以同时实现多个接口。它们用来定义规范、做多态。

**操作**

```php
<?php
interface Shape {
    public function area(): float;
}
abstract class Base {
    abstract public function name(): string;
}
class Circle extends Base implements Shape {
    public function __construct(private float $r) {}
    public function area(): float {
        return 3.14 * $this->r * $this->r;
    }
    public function name(): string {
        return "圆";
    }
}
$c = new Circle(2);
echo $c->name() . " 面积=" . $c->area() . "\n";
// 运行结果：
// 圆 面积=12.56
```

### `魔术方法` 被特殊触发的方法🔒

**解析**　以 `__` 开头的方法会在特定操作时**自动调用**：`__get`/`__set` 读写不可见属性、`__isset`/`__unset` 配合 isset/unset、`__toString` 对象当字符串用、`__invoke` 对象当函数调用、`__call` 调不存在的方法。框架和 ORM 大量使用。

**操作**

```php
<?php
class Box {
    private array $data = [];
    public function __set($k, $v) { $this->data[$k] = $v; }
    public function __get($k) { return $this->data[$k] ?? "无"; }
    public function __toString() { return "Box(" . implode(",", $this->data) . ")"; }
}
$b = new Box();
$b->color = "red";
echo $b->color . "\n";
echo $b->size . "\n";
echo $b . "\n";
// 运行结果：
// red
// 无
// Box(red)
```

> ⚠️ `__toString` 里不能抛异常（会致命错误）；反序列化场景里 `__wakeup`、`__destruct`、`__toString` 常被串成"POP 链"执行代码——审计时重点看这几个。

### `命名空间` 隔离同名的类与函数

**解析**　命名空间给类/函数/常量套一层前缀，避免和别处的同名冲突（类似目录）。用 `namespace App\Models;` 声明，`use App\Models\User;` 引入，`::class` 取完全限定名。分隔符是**反斜杠 `\`**，不是 `/`。

**操作**

```php
<?php
namespace App\Models;
class User {
    public function name() { return "User 实例"; }
}
namespace App;
$u = new \App\Models\User();
echo $u->name() . "\n";
echo \App\Models\User::class . "\n";
// 运行结果：
// User 实例
// App\Models\User
```

> ⚠️ `namespace` 必须是文件里（除 declare 外）第一条语句，前面不能有输出。完全限定名以 `\` 开头，写漏了会被当相对路径去找。

### `trait` 横向复用方法

**解析**　trait 是一组可被多个类**横向复用**的方法（解决 PHP 单继承的局限）：定义用 `trait 名 { ... }`，类里用 `use 名;` 引入，效果就像把这些方法抄进类里。类可以同时 `use` 多个 trait。

**操作**

```php
<?php
trait Greetable {
    public function greet() {
        return "你好，我是 " . $this->name;
    }
}
class User {
    use Greetable;
    public function __construct(public string $name) {}
}
$u = new User("小明");
echo $u->greet() . "\n";
// 运行结果：
// 你好，我是 小明
```

> ⚠️ trait 里可以直接访问 `$this` 的属性/方法，所以它会**隐式依赖**宿主类有 `$this->name` 之类成员——换到没有该成员的类上就会报错，用之前想清楚约定。

## 八 错误与异常处理

### `错误报告` 打开与关闭报错🔒

**解析**　PHP 的报错分级别：`E_WARNING` 警告（继续跑）、`E_NOTICE` 提示、`E_ERROR` 致命错误（停下）、`E_DEPRECATED` 过时警告。开发时用 `error_reporting(E_ALL)` + `ini_set("display_errors", "1")` 把错误都显示出来；上线必须关掉显示、只写日志，否则报错信息会泄露路径和代码。

**操作**

```php
<?php
error_reporting(E_ALL);
ini_set("display_errors", "1");
ini_set("log_errors", "0");      // 只显示、不另写日志，避免重复
echo $undefined;                 // 未定义变量 → 警告
echo "出错后仍继续执行\n";
// 运行结果：
//
// Warning: Undefined variable $undefined in /Users/zhangzixin/.hermes/cache/scratch/phpnote/run/snip.php on line 5
// 出错后仍继续执行
```

> ⚠️ 生产环境 `display_errors=Off` 是基本要求：报错会泄露**绝对路径、数据库账号、SQL 语句**，是渗透的信息收集点。关掉显示、用 `log_errors=On` 写日志。

### `try、catch、finally` 捕获异常与收尾

**解析**　把可能出错的代码放进 `try`，出错抛出的异常用 `catch (异常类型 $e)` 接住，`finally` 里的代码**无论是否出错都会执行**（用来关连接、清资源）。一个 try 可以配多个 catch 接不同异常。

**操作**

```php
<?php
function divide($a, $b) {
    if ($b == 0) {
        throw new Exception("除数不能为 0");
    }
    return $a / $b;
}
try {
    echo divide(10, 2) . "\n";
    echo divide(10, 0) . "\n";      // 这里抛异常，后面不再执行
} catch (Exception $e) {
    echo "捕获异常：" . $e->getMessage() . "\n";
} finally {
    echo "finally 总会执行\n";
}
// 运行结果：
// 5
// 捕获异常：除数不能为 0
// finally 总会执行
```

### `throw` 按类型抛出异常

**解析**　`throw new 异常类(消息, 代码)` 主动抛出异常，向上层传递。内置异常类型很多：`InvalidArgumentException`（参数不合法）、`RangeException`（超出范围）、`RuntimeException`、`TypeError`……用不同类型的 catch 分开处理，代码更清楚。

**操作**

```php
<?php
function setAge($age) {
    if (!is_int($age)) {
        throw new InvalidArgumentException("年龄必须是整数");
    }
    if ($age < 0) {
        throw new RangeException("年龄不能为负");
    }
    return $age;
}
foreach ([18, "18", -1] as $a) {
    try {
        echo "设置成功：" . setAge($a) . "\n";
    } catch (InvalidArgumentException $e) {
        echo "参数错误：" . $e->getMessage() . "\n";
    } catch (RangeException $e) {
        echo "范围错误：" . $e->getMessage() . "\n";
    }
}
// 运行结果：
// 设置成功：18
// 参数错误：年龄必须是整数
// 范围错误：年龄不能为负
```

### `自定义异常类` 继承 Exception 定义错误

**解析**　自己写一个异常类，只要 `extends Exception` 就行，可以加自己的方法/属性。团队里约定"业务异常""校验异常"各自一个类，catch 时就能精确区分错误来源。

**操作**

```php
<?php
class MyException extends Exception {
    public function tip() { return "【业务异常】"; }
}
try {
    throw new MyException("余额不足", 500);
} catch (MyException $e) {
    echo $e->tip() . $e->getMessage() . "\n";
    echo "错误码：" . $e->getCode() . "\n";
}
// 运行结果：
// 【业务异常】余额不足
// 错误码：500
```

### `set_error_handler` 把错误变成自定义处理

**解析**　`set_error_handler(回调)` 接管"警告/提示"级别的错误（致命错误接管不了）。回调里可以记日志、或把错误转成异常抛出。返回 `true` 表示"已处理"，不再走 PHP 默认的报错。

**操作**

```php
<?php
set_error_handler(function ($level, $msg, $file, $line) {
    echo "抓到错误：$msg\n";
    return true;   // 已处理，不再默认报错
});
trigger_error("这是一个测试错误", E_USER_WARNING);
echo "继续执行\n";
// 运行结果：
// 抓到错误：这是一个测试错误
// 继续执行
```

### `error_log` 把错误写进日志文件

**解析**　`error_log(消息, 类型, 目标)` 把一条消息写进日志文件、系统日志或发邮件。生产环境靠它记录错误和可疑请求，是排查和安全审计的依据。

**操作**

```php
<?php
$log = __DIR__ . "/app.log";
ini_set("error_log", $log);
error_log("用户登录失败");
error_log("数据库超时");
foreach (file($log, FILE_IGNORE_NEW_LINES) as $line) {
    echo preg_replace('/^\[[^\]]*\]\s*/', '', $line) . "\n";   // 去掉行首时间戳
}
unlink($log);
// 运行结果：
// 用户登录失败
// 数据库超时
```

## 九 文件与目录操作

### `文件读写函数` 整文件读与写🔒

**解析**　`file_get_contents(路径)` 把整个文件读成字符串，`file_put_contents(路径, 内容)` 把字符串写进文件（默认覆盖，`FILE_APPEND` 追加）。比 `fopen/fread/fwrite` 那套简单，日常够用。

**操作**

```php
<?php
$f = __DIR__ . "/demo.txt";
file_put_contents($f, "hello world\n");
echo file_get_contents($f);
var_dump(file_exists($f));
unlink($f);
var_dump(file_exists($f));
// 运行结果：
// hello world
// bool(true)
// bool(false)
```

> ⚠️ 路径可控时极其危险：`file_get_contents($_GET["f"])` 就是"任意文件读取"；`file_put_contents("shell.php", $_GET["c"])` 能直接写出一个 webshell。用户输入绝不能拼进文件路径。

### `fopen、fwrite、fread、fclose` 按句柄打开读写关闭

**解析**　`fopen(路径, 模式)` 打开文件返回句柄，`fwrite` 写、`fread` 读、`fgets` 读一行，最后 `fclose` 关闭。模式：`r` 只读、`w` 覆盖写、`a` 追加写、`r+` 读写。大文件、按行处理、需要精确控制指针时用它。

**操作**

```php
<?php
$f = __DIR__ . "/data.txt";
$fp = fopen($f, "w");
fwrite($fp, "第一行\n第二行\n");
fclose($fp);
$fp = fopen($f, "r");
echo fread($fp, filesize($f));
fclose($fp);
unlink($f);
// 运行结果：
// 第一行
// 第二行
```

> ⚠️ `w` 模式会因为**打开即清空**，一不留神就把文件清空了；追加内容要用 `a`。写完记得 `fclose`，否则可能没落盘。

### `file` 把文件按行读成数组

**解析**　`file(路径)` 把整个文件读成一个数组，**每个元素是一行**（默认带换行符）。加 `FILE_IGNORE_NEW_LINES` 去掉行尾换行、`FILE_SKIP_EMPTY_LINES` 跳过空行。读配置、读单词表、逐行处理很方便。

**操作**

```php
<?php
$f = __DIR__ . "/lines.txt";
file_put_contents($f, "apple\nbanana\ncherry\n");
$lines = file($f, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
print_r($lines);
echo "行数：" . count($lines) . "\n";
unlink($f);
// 运行结果：
// Array
// (
//     [0] => apple
//     [1] => banana
//     [2] => cherry
// )
// 行数：3
```

### `文件与目录函数` 判断、删除、建目录、列目录

**解析**　`file_exists` 是否存在、`is_file`/`is_dir` 是文件还是目录、`unlink` 删文件、`mkdir` 建目录、`rmdir` 删空目录、`scandir` 列目录内容（结果**包含 `.` 和 `..`**）、`filesize` 大小、`copy`/`rename` 复制改名。

**操作**

```php
<?php
$dir = __DIR__ . "/testdir";
mkdir($dir);
echo is_dir($dir) ? "目录已建" : "失败";
echo "\n";
file_put_contents($dir . "/a.txt", "1");
file_put_contents($dir . "/b.txt", "2");
print_r(scandir($dir));
unlink($dir . "/a.txt");
unlink($dir . "/b.txt");
rmdir($dir);
echo is_dir($dir) ? "还在" : "已删除";
echo "\n";
// 运行结果：
// 目录已建
// Array
// (
//     [0] => .
//     [1] => ..
//     [2] => a.txt
//     [3] => b.txt
// )
// 已删除
```

> ⚠️ `scandir` 结果里有 `.`（自己）和 `..`（上级），遍历时要先过滤，否则容易出问题。删目录前必须先把里面清空（`rmdir` 只删空目录）。

### `include 与 require` 文件包含🔒

**解析**　把一个文件的内容插进来，常放公共函数、配置、页头页尾。区别：`include` 找不到只报警告、继续跑；`require` 找不到直接**致命错误停止**；带 `_once` 的保证同一文件只被包含一次。

**操作**

```php
<?php
file_put_contents(__DIR__ . "/config.php", "<?php \$host = \"localhost\"; \$user = \"root\";");
include __DIR__ . "/config.php";
echo $host . "\n";
require_once __DIR__ . "/config.php";
echo "require_once 不会重复包含\n";
unlink(__DIR__ . "/config.php");
// 运行结果：
// localhost
// require_once 不会重复包含
```

> ⚠️ **头号漏洞（文件包含 LFI/RFI）**：如果路径带用户输入，例如 `include $_GET["page"];`，攻击者传 `?page=/etc/passwd` 就能读任意文件，配合文件上传或日志还能执行代码（RCE）。防御：用白名单固定页名，绝不把用户输入直接拼进 include。

### `路径处理` 拆解文件路径🔒

**解析**　`basename()` 取文件名，`dirname()` 取所在目录，`pathinfo()` 拆成 `dirname`/`basename`/`extension`/`filename` 四部分（第二参数可只取某一项），`realpath()` 转成规范化的绝对路径。

**操作**

```php
<?php
$p = "/var/www/html/index.php";
echo basename($p) . "\n";
echo dirname($p) . "\n";
print_r(pathinfo($p));
echo pathinfo($p, PATHINFO_EXTENSION) . "\n";
// 运行结果：
// index.php
// /var/www/html
// Array
// (
//     [dirname] => /var/www/html
//     [basename] => index.php
//     [extension] => php
//     [filename] => index
// )
// php
```

> ⚠️ `basename()` 常被用来"防目录穿越"（只取文件名），但要注意它在某些系统上会被 `..` 或非 ASCII 绕过，安全场景别只依赖它，配合白名单。

### `glob` 按通配符查找文件

**解析**　`glob(模式)` 按通配符返回匹配的文件路径数组，支持 `*`（任意）、`?`（一个字符）、`[abc]`（字符集）、`{a,b}`（大括号里的任一，需 `GLOB_BRACE`）。找某个后缀的文件很方便。

**操作**

```php
<?php
$dir = __DIR__ . "/g";
mkdir($dir);
file_put_contents($dir . "/a.log", "");
file_put_contents($dir . "/b.txt", "");
file_put_contents($dir . "/c.log", "");
foreach (glob($dir . "/*.log") as $f) {
    echo basename($f) . "\n";
}
array_map("unlink", glob($dir . "/*"));
rmdir($dir);
// 运行结果：
// a.log
// c.log
```

### `读写 JSON 文件` 结构化数据存盘

**解析**　把数组/对象用 `json_encode()` 变成 JSON 字符串写进文件，读的时候 `file_get_contents()` 再 `json_decode($s, true)` 还原成数组——这是最常用的轻量"数据库"。`JSON_UNESCAPED_UNICODE` 让中文不被转成 `\uXXXX`。

**操作**

```php
<?php
$data = ["name" => "小明", "tags" => ["php", "web"]];
$f = __DIR__ . "/data.json";
file_put_contents($f, json_encode($data, JSON_UNESCAPED_UNICODE));
echo file_get_contents($f) . "\n";
$back = json_decode(file_get_contents($f), true);
echo $back["tags"][0] . "\n";
unlink($f);
// 运行结果：
// {"name":"小明","tags":["php","web"]}
// php
```

> ⚠️ `json_decode` 第二个参数传 `true` 才返回**数组**，不传返回对象（要用 `->` 访问）。读别人写的 JSON 记得判断 `json_last_error()`，解析失败会返回 `null` 而不是报错。

## 十 表单与超全局变量（Web 请求）

### `$_GET` 取地址栏参数🔒

**解析**　$_GET 是**超全局数组**（函数内外都能直接用），装 URL 里 `?id=1&name=admin` 这样的参数。安全用途：这些值**完全由用户控制**，直接拿去查询/拼接/包含就是漏洞入口——`$_GET["cmd"]` 进了 `system()` 就是命令执行，`$_GET["page"]` 进了 `include()` 就是任意文件包含。

**操作**

```php
<?php
echo "id=" . ($_GET["id"] ?? "无") . "\n";
echo "name=" . ($_GET["name"] ?? "无") . "\n";
echo "age=" . ($_GET["age"] ?? "无") . "\n";
// 实跑请求：curl -s "http://127.0.0.1:8765/w_get.php?id=1&name=admin"
// 运行结果：
// id=1
// name=admin
// age=无
```

> ⚠️ 没传的键会报 `Undefined array key` 警告，用 `?? "默认值"` 兜底。`$_GET` 里的值**永远是字符串**，需要整数记得 `(int)` 转换。

### `$_POST` 取表单提交的数据🔒

**解析**　表单用 `method="post"` 提交时，数据放在 `$_POST` 里、**不出现在 URL 上**，适合传密码、长内容。取值方式跟 `$_GET` 一样。安全用途同 `$_GET`：内容用户可控，拼进危险函数照样是漏洞。

**操作**

```php
<?php
echo "user=" . ($_POST["user"] ?? "无") . "\n";
echo "pass=" . ($_POST["pass"] ?? "无") . "\n";
// 实跑请求：curl -s -d "user=xiaoming&pass=123456" "http://127.0.0.1:8765/w_post.php"
// 运行结果：
// user=xiaoming
// pass=123456
```

> ⚠️ POST 比 GET 安全只是"不显示在地址栏"，**照样能被篡改、照样是用户输入**。别把"用了 POST"当成安全，参数化/白名单才是。

### `$_REQUEST` 一次取 GET POST Cookie🔒

**解析**　$_REQUEST 把 GET、POST、Cookie 里的参数**合并**在一起，取哪个都行，写起来方便。但正因如此你**不知道取到的值到底来自哪里**，容易被参数污染绕过。

**操作**

```php
<?php
echo "q=" . ($_REQUEST["q"] ?? "无") . "\n";
// 实跑请求：curl -s "http://127.0.0.1:8765/w_request.php?q=hello"
// 运行结果：
// q=hello
```

> ⚠️ 能明确来源就用 `$_GET` 或 `$_POST`，别用 `$_REQUEST`。它受 `request_order` 配置影响，同名参数"谁覆盖谁"不确定，审计时经常是绕过点。

### `$_COOKIE` 取浏览器的 Cookie🔒

**解析**　浏览器每次请求都会带上 Cookie，服务器用 `$_COOKIE` 读。常用来存 session id 或"记住我"的 token。安全用途：Cookie **存在客户端、用户可以随便改**，绝不能拿 Cookie 里的值当"已验证"的凭据。

**操作**

```php
<?php
echo "token=" . ($_COOKIE["token"] ?? "无 cookie") . "\n";
// 实跑请求：curl -s -b "token=abc123" "http://127.0.0.1:8765/w_cookie.php"
// 运行结果：
// token=abc123
```

> ⚠️ `if ($_COOKIE["is_admin"] == 1) { ... }` 这种判断，攻击者自己加一条 Cookie 就绕过了——权限必须存在服务器端（session / 数据库）。

### `$_SERVER` 服务器与请求信息🔒

**解析**　装服务器和执行环境的信息。常用的：`REQUEST_METHOD`（GET/POST）、`REMOTE_ADDR`（客户端 IP）、`SCRIPT_NAME`（当前脚本路径）、`QUERY_STRING`（问号后的原始串）、`HTTP_USER_AGENT`（浏览器标识）、`DOCUMENT_ROOT`（网站根目录）。写日志、判断请求来源常用。

**操作**

```php
<?php
echo "METHOD=" . $_SERVER["REQUEST_METHOD"] . "\n";
echo "SCRIPT=" . $_SERVER["SCRIPT_NAME"] . "\n";
echo "QUERY=" . ($_SERVER["QUERY_STRING"] ?? "") . "\n";
echo "AGENT=" . ($_SERVER["HTTP_USER_AGENT"] ?? "") . "\n";
echo "REMOTE=" . $_SERVER["REMOTE_ADDR"] . "\n";
// 实跑请求：curl -s -A "MyBrowser/1.0" "http://127.0.0.1:8765/w_server.php?a=1"
// 运行结果：
// METHOD=GET
// SCRIPT=/w_server.php
// QUERY=a=1
// AGENT=MyBrowser/1.0
// REMOTE=127.0.0.1
```

> ⚠️ `REMOTE_ADDR` 来自 TCP 连接、不好伪造；`HTTP_X_FORWARDED_FOR` 这类请求头是**客户端可伪造**的，别用它做 IP 白名单，否则头加一行就绕过。

### `$_ENV 与环境变量` 读写环境变量🔒

**解析**　`getenv("名字")` 读环境变量，`putenv("名字=值")` 设一个。`$_ENV` 是环境变量数组，但它是否被填充取决于 `variables_order` 配置（很多环境默认不含 `E`，所以 `$_ENV` 可能是空的）。配置项、密钥通常放环境变量里，别写死在代码中。

**操作**

```php
<?php
putenv("APP_ENV=production");
echo getenv("APP_ENV") . "\n";
echo ($_ENV["APP_ENV"] ?? '（$_ENV 默认不含它，用 getenv 更稳）');
var_dump(getenv("PATH") !== false);
// 运行结果：
// production
// （$_ENV 默认不含它，用 getenv 更稳）bool(true)
```

> ⚠️ 数据库密码、API 密钥**别写死在代码里**再提交上去（这是最常见的泄露源）。用环境变量或 `.env` 文件，并确保 `.env` 进了 `.gitignore`。

### `$_FILES` 接收上传的文件🔒

**解析**　表单带 `enctype="multipart/form-data"` 提交的文件放在 `$_FILES["字段名"]` 里，是一个数组：`name` 原文件名、`tmp_name` 服务器临时路径、`size` 字节数、`error` 错误码（`0` = 成功）。用 `move_uploaded_file()` 把临时文件挪到你要保存的位置。

**操作**

```php
<?php
$f = $_FILES["up"];
echo "name=" . $f["name"] . "\n";
echo "size=" . $f["size"] . "\n";
echo "error=" . $f["error"] . "\n";
move_uploaded_file($f["tmp_name"], __DIR__ . "/uploads/" . $f["name"]);
echo "saved=" . (file_exists(__DIR__ . "/uploads/" . $f["name"]) ? "yes" : "no") . "\n";
// 实跑请求：curl -s -F "up=@upload_test.txt" "http://127.0.0.1:8765/w_files.php"
// 运行结果：
// name=upload_test.txt
// size=12
// error=0
// saved=yes
```

> ⚠️ `name`、`type` 全由**用户控制**，直接拿去拼保存路径会有路径穿越（`../../shell.php`）或任意文件上传。要：扩展名白名单、自己重命名文件、把保存目录设成不可执行。

### `php://input` 读取原始请求体🔒

**解析**　`file_get_contents("php://input")` 读**未经解析的原始请求体**。当请求不是表单（比如 `Content-Type: application/json`、`text/xml`），`$_POST` 是空的，就得从这里取原始数据再自己 `json_decode`。这也是接收 Webhook、API 请求的标准方式。

**操作**

```php
<?php
$raw = file_get_contents("php://input");
echo "raw=" . $raw . "\n";
// 实跑请求：curl -s -d "raw_body_data" "http://127.0.0.1:8765/w_input.php"
// 运行结果：
// raw=raw_body_data
```

> ⚠️ `php://input` 只能读一次、且和 `$_POST` 互斥：表单提交（`application/x-www-form-urlencoded`）时 PHP 已经读过它填进 `$_POST` 了。PHP 5.6+ 起它可重复读。

### `filter_var` 校验与过滤输入🔒

**解析**　`filter_var($值, 过滤器)` 校验/过滤单个值。校验类失败返回 `false`：`FILTER_VALIDATE_EMAIL`、`FILTER_VALIDATE_IP`、`FILTER_VALIDATE_INT`、`FILTER_VALIDATE_URL`。`FILTER_SANITIZE_*` 会清洗掉非法字符。它是把"用户输入"规范化的一道防线。

**操作**

```php
<?php
var_dump(filter_var("test@example.com", FILTER_VALIDATE_EMAIL) !== false);
var_dump(filter_var("not-an-email", FILTER_VALIDATE_EMAIL));
var_dump(filter_var("127.0.0.1", FILTER_VALIDATE_IP));
var_dump(filter_var("abc", FILTER_VALIDATE_INT));
echo filter_var("http://x.com/?a=1 ", FILTER_SANITIZE_URL) . "\n";
// 运行结果：
// bool(true)
// bool(false)
// string(9) "127.0.0.1"
// bool(false)
// http://x.com/?a=1
```

> ⚠️ `FILTER_VALIDATE_*` 校验失败返回 `false`，但合法值也可能是 `0`/`false` 这种"假值"——判断要用 `!== false`。别把 filter_var 当唯一防线，它只管格式，不防业务逻辑绕过。

### `htmlspecialchars` 输出转义防 XSS🔒

**解析**　把用户输入**输出到 HTML 页面之前**，用 `htmlspecialchars($s, ENT_QUOTES, "UTF-8")` 把 `<` `>` `&` `"` `'` 转成实体，浏览器就只会把它们当文字显示、不会当标签执行。这是防 XSS 的标准做法。

**操作**

```php
<?php
$x = $_GET["x"] ?? "";
echo "原始: " . $x . "\n";
echo "转义: " . htmlspecialchars($x, ENT_QUOTES, "UTF-8") . "\n";
// 实跑请求：curl -s -G --data-urlencode "x=<script>alert(1)</script>" "http://127.0.0.1:8765/w_escape.php"
// 运行结果：
// 原始: <script>alert(1)</script>
// 转义: &lt;script&gt;alert(1)&lt;/script&gt;
```

> ⚠️ **防 XSS 抓输出不抓输入**：同一个值可能在 HTML、属性、JS、URL 里，共用一套转义会漏。HTML 正文用 `htmlspecialchars`，URL 参数用 `urlencode`，属性值要加引号。绝不 `echo $_GET["x"]` 直接输出。

## 十一 会话与 Cookie

### `$_SESSION` 跨页面保存登录状态🔒

**解析**　session 数据存在**服务器端**，浏览器只拿一个 session id（通常放在 Cookie 里）。用之前**必须 `session_start()`**，之后像普通数组一样读写 `$_SESSION`。登录成功后把用户信息存进去，其它页面就能读到。

**操作**

```php
<?php
session_start();
$_SESSION["count"] = ($_SESSION["count"] ?? 0) + 1;
echo "count=" . $_SESSION["count"] . "\n";
// 实跑请求：rm -f /tmp/pnjar && curl -s -c /tmp/pnjar -b /tmp/pnjar "http://127.0.0.1:8765/w_session.php"
// 运行结果：
// count=1
// count=2
```

> ⚠️ session id 被偷（XSS 或没设 HttpOnly Cookie）就等于对方登录了你的账号；登录成功后应执行 `session_regenerate_id(true);` 换 id，防"会话固定"。

### `session_regenerate_id 与 session_destroy` 换 id 与登出🔒

**解析**　`session_regenerate_id(true)` 立即把当前 session id 换成新的（旧的作废）——**登录成功后必须调用**，防会话固定攻击。`session_destroy()` 销毁服务器端 session（登出）。`session_unset()` 清空 `$_SESSION` 但保留会话。

**操作**

```php
<?php
session_start();
$old = session_id();
$_SESSION["user"] = "admin";
session_regenerate_id(true);
$new = session_id();
echo "登录用户：" . $_SESSION["user"] . "\n";
echo "sid 已更换：" . ($old !== $new ? "是" : "否") . "\n";
echo "换 id 后 session 数据仍在：" . $_SESSION["user"] . "\n";
// 实跑请求：curl -s "http://127.0.0.1:8765/w_login.php"
// 运行结果：
// 登录用户：admin
// sid 已更换：是
// 换 id 后 session 数据仍在：admin
```

> ⚠️ 忘了 `session_regenerate_id(true)` 会给"会话固定"留口子：攻击者先诱导你用一个他已知的 session id 登录，之后他就拿着这个 id 冒充你。登出要 `session_destroy()` 并把 Cookie 也清掉。

### `setcookie` 发送 Cookie 给浏览器🔒

**解析**　`setcookie(名字, 值, 选项)` 让浏览器保存一条 Cookie。安全相关选项：`httponly => true`（JS 读不到，防 XSS 偷 cookie）、`secure => true`（只在 HTTPS 传）、`samesite => "Strict"/"Lax"`（防 CSRF）。**必须在任何输出之前调用**。

**操作**

```php
<?php
setcookie("token", "abc123", ["httponly" => true, "samesite" => "Strict"]);
echo "已发送 Cookie: token=abc123\n";
// 实跑请求：curl -s -D - -o /dev/null "http://127.0.0.1:8765/w_setcookie.php" | grep -i "^set-cookie"
// 运行结果：
// Set-Cookie: token=abc123; HttpOnly; SameSite=Strict
```

> ⚠️ Cookie 里**不要存**敏感明文（密码、权限标志）；session cookie 一定要 `HttpOnly`+`Secure`+`SameSite`，否则 XSS 一条 `document.cookie` 就能把登录态偷走。

## 十二 数据库操作

### `mysqli 连接数据库` 连接 MySQL 并查询🔒

**解析**　`mysqli` 是连 MySQL 的常用扩展：`mysqli_connect(主机, 用户, 密码, 库名, 端口)` 建连接，`mysqli_query()` 执行 SQL，`mysqli_fetch_assoc()` 一行行取结果（返回关联数组），最后 `mysqli_close()` 关闭。下面这段**真的连了本机 MySQL 8.4.11 的 `php_demo` 库**。

**操作**

```php
<?php
$conn = mysqli_connect("127.0.0.1", "root", "", "php_demo", 3306);
if (!$conn) {
    die("连接失败：" . mysqli_connect_error());
}
$res = mysqli_query($conn, "SELECT id, username, email FROM users");
while ($row = mysqli_fetch_assoc($res)) {
    echo $row["id"] . " " . $row["username"] . " " . $row["email"] . "\n";
}
mysqli_close($conn);
// 运行结果：
// 1 admin admin@demo.local
// 2 alice alice@demo.local
// 3 bob bob@demo.local
```

> ⚠️ 别把用户输入拼进 SQL：`"SELECT * FROM users WHERE id = " . $_GET["id"]` 就是 **SQL 注入**。要么用 `mysqli_real_escape_string()` 转义，要么直接用预处理（下一条）。连库失败时别把 `mysqli_connect_error()` 输出给用户，会泄露账号/主机信息。

### `mysqli 预处理查询` 防 SQL 注入（mysqli 版）🔒

**解析**　预处理：SQL 里用 `?` 占位，`mysqli_prepare()` 编译好语句，`mysqli_stmt_bind_param($stmt, "i", $id)` 单独绑定值（`"i"` 整数 / `"s"` 字符串 / `"d"` 小数 / `"b"` 二进制），再 `execute()`。数据库把"语句"和"数据"分开处理，注入无效。

**操作**

```php
<?php
$conn = mysqli_connect("127.0.0.1", "root", "", "php_demo", 3306);
$stmt = mysqli_prepare($conn, "SELECT username FROM users WHERE id = ?");
$id = 2;
mysqli_stmt_bind_param($stmt, "i", $id);
mysqli_stmt_execute($stmt);
$res = mysqli_stmt_get_result($stmt);
while ($row = mysqli_fetch_assoc($res)) {
    echo "查询结果：" . $row["username"] . "\n";
}
mysqli_close($conn);
// 运行结果：
// 查询结果：alice
```

> ⚠️ 占位符**只对"值"有效**：表名、列名、`ORDER BY` 后面的字段没法用 `?`（会报错），这些位置只能靠白名单校验。千万别为了省事把注入点挪到表名/列名上。

### `PDO 连接数据库` 连接 MySQL 并查询（PDO 版）🔒

**解析**　`new PDO(dsn, 用户, 密码)` 建立连接，DSN 形如 `mysql:host=...;port=3306;dbname=...;charset=utf8mb4`。`query()` 执行查询、`fetchAll(PDO::FETCH_COLUMN)` 直接取某一列。设 `PDO::ATTR_ERRMODE => ERRMODE_EXCEPTION` 让出错抛异常、好排查。PDO 的好处是**同一套代码能换数据库**。

**操作**

```php
<?php
$pdo = new PDO("mysql:host=127.0.0.1;port=3306;dbname=php_demo;charset=utf8mb4", "root", "");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$rows = $pdo->query("SELECT username FROM users ORDER BY id")->fetchAll(PDO::FETCH_COLUMN);
print_r($rows);
echo "驱动：" . $pdo->getAttribute(PDO::ATTR_DRIVER_NAME) . "\n";
// 运行结果：
// Array
// (
//     [0] => admin
//     [1] => alice
//     [2] => bob
// )
// 驱动：mysql
```

> ⚠️ DSN 里一定带 `charset=utf8mb4`，否则中文可能被存成乱码/被截断。别把用户名密码写死在代码里提交到仓库，用配置文件+环境变量。

### `PDO 预处理查询` 防 SQL 注入（PDO 版）🔒

**解析**　推荐写法：`$pdo->prepare("SELECT ... WHERE id = ?")` 再用 `$stmt->execute([$id])` 把值单独传进去。也可以用命名占位 `:id`，`execute([":id" => $id])`。数据库分开处理"语句"和"数据"，注入无效——这是防 SQL 注入的标准做法。

**操作**

```php
<?php
$pdo = new PDO("mysql:host=127.0.0.1;dbname=php_demo;charset=utf8mb4", "root", "");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$stmt = $pdo->prepare("SELECT username FROM users WHERE id = ?");
$stmt->execute([3]);
echo "结果：" . $stmt->fetchColumn() . "\n";
// ❌ 危险写法：把用户输入拼进 SQL（会注入）
// $pdo->query("SELECT * FROM users WHERE id = " . $_GET["id"]);
// 运行结果：
// 结果：bob
```

> ⚠️ **用了预处理就不能再拼字符串**：一旦写成 `"... WHERE id='" . $_GET['id'] . "'"`，预处理就白做了。审计时重点看有没有 `query()` 里直接拼变量。

### `PDO 事务` 提交与回滚

**解析**　事务保证一组 SQL **要么全成功、要么全不做**。`beginTransaction()` 开始，之后 `commit()` 提交、或 `rollBack()` 撤销。转账、下订单这类"改多张表"的操作必须用事务，出错时回滚避免数据不一致。

**操作**

```php
<?php
$pdo = new PDO("mysql:host=127.0.0.1;dbname=php_demo;charset=utf8mb4", "root", "");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$pdo->exec("CREATE TABLE IF NOT EXISTS t_tx (id INT, amount INT)");
$pdo->exec("DELETE FROM t_tx");
$pdo->beginTransaction();
$pdo->exec("INSERT INTO t_tx VALUES (1, 100)");
$pdo->exec("INSERT INTO t_tx VALUES (2, 200)");
$pdo->rollBack();      // 撤销上面的插入
echo "回滚后行数：" . $pdo->query("SELECT COUNT(*) FROM t_tx")->fetchColumn() . "\n";
$pdo->beginTransaction();
$pdo->exec("INSERT INTO t_tx VALUES (1, 100)");
$pdo->commit();        // 真正写入
echo "提交后行数：" . $pdo->query("SELECT COUNT(*) FROM t_tx")->fetchColumn() . "\n";
$pdo->exec("DROP TABLE t_tx");
// 运行结果：
// 回滚后行数：0
// 提交后行数：1
```

> ⚠️ 事务要作用在**支持事务的存储引擎**上：MySQL 的 MyISAM 不支持，只有 InnoDB 才回滚得了。另外别在事务里做太耗时的操作（比如等网络），会长时间锁行。

### `查询结果处理` fetch 家族怎么取数据

**解析**　PDO 取结果用 `fetch(PDO::FETCH_ASSOC)` 取一行（关联数组）、`fetchAll()` 取全部行、`fetchColumn()` 取第一列的值（适合 `COUNT(*)`）、`rowCount()` 受影响行数。常配 `FETCH_CLASS` 直接把行映射成对象。

**操作**

```php
<?php
$pdo = new PDO("mysql:host=127.0.0.1;dbname=php_demo;charset=utf8mb4", "root", "");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$stmt = $pdo->query("SELECT id, username FROM users ORDER BY id");
print_r($stmt->fetch(PDO::FETCH_ASSOC));      // 第一行
print_r($stmt->fetchAll(PDO::FETCH_COLUMN, 1)); // 剩余行的第 1 列
echo "总数：" . $pdo->query("SELECT COUNT(*) FROM users")->fetchColumn() . "\n";
// 运行结果：
// Array
// (
//     [id] => 1
//     [username] => admin
// )
// Array
// (
//     [0] => alice
//     [1] => bob
// )
// 总数：3
```

## 十三 时间、JSON 与加密

### `时间函数` date、time、strtotime

**解析**　`time()` 取当前时间戳（从 1970-01-01 UTC 起的秒数），`date(格式, 时间戳)` 把时间戳格式化成字符串，`strtotime("表达式")` 把字符串/自然语言（`"+7 days"`）转成时间戳。输出时区由 `date_default_timezone_set()` 决定。

**操作**

```php
<?php
date_default_timezone_set("Asia/Shanghai");
$t = 1700000000;                      // 固定的时间戳
echo date("Y-m-d H:i:s", $t) . "\n";
echo date("Y-m-d", strtotime("+7 days", $t)) . "\n";
echo strtotime("2026-01-01 00:00:00") . "\n";
// 运行结果：
// 2023-11-15 06:13:20
// 2023-11-22
// 1767196800
```

> ⚠️ `date()` 输出的**时区**默认可能不是你要的（不设就按 `date.timezone` 配置，本机未设则用 UTC），生产环境务必显式 `date_default_timezone_set("Asia/Shanghai")` 或写死 `date.timezone`。`time()` 返回的是"当前"时间戳，每次跑都不同。

### `DateTime 类` 面向对象方式处理日期

**解析**　`new DateTime(字符串, 时区)` 造一个日期对象，`format()` 输出、`modify("+1 month")` 加减、`diff()` 算两个日期的差（`->days` 是天数）、`setTimestamp()` 从时间戳设。比一堆 `date`/`strtotime` 函数更清晰、支持时区切换。

**操作**

```php
<?php
$d = new DateTime("2026-10-08 12:00:00", new DateTimeZone("Asia/Shanghai"));
echo $d->format("Y年m月d日 H:i") . "\n";
$d->modify("+1 month");
echo "加一个月：" . $d->format("Y-m-d") . "\n";
$d2 = new DateTime("2026-01-01", new DateTimeZone("Asia/Shanghai"));
echo "相差天数：" . $d->diff($d2)->days . "\n";
// 运行结果：
// 2026年10月08日 12:00
// 加一个月：2026-11-08
// 相差天数：311
```

> ⚠️ `modify("+1 month")` 是"加一个月"不是"加 30 天"，跨月末的结果可能反直觉（比如 3-31 加一个月可能落到 5-01）。

### `JSON 编解码` json_encode 与 json_decode

**解析**　`json_encode($值)` 把数组/对象变成 JSON 字符串；`json_decode($s, true)` 把 JSON 变回**数组**（不传 `true` 返回对象）。`JSON_UNESCAPED_UNICODE` 保留中文可读性。前后端、接口、缓存到处是 JSON。

**操作**

```php
<?php
$data = ["name" => "小明", "age" => 18, "tags" => ["php", "web"]];
$json = json_encode($data, JSON_UNESCAPED_UNICODE);
echo $json . "\n";
$back = json_decode($json, true);
echo $back["tags"][1] . "\n";
$obj = json_decode($json);          // 不传 true → 对象
echo $obj->name . "\n";
var_dump(json_decode("{这是一个坏 json"));
echo json_last_error_msg() . "\n";
// 运行结果：
// {"name":"小明","age":18,"tags":["php","web"]}
// web
// 小明
// NULL
// Syntax error
```

> ⚠️ 解析失败时 `json_decode` 返回 `null` 而**不报错**，必须用 `json_last_error()` / `json_last_error_msg()` 检查。参数传 `true` 才是数组，否则是对象、取值用 `->`。

### `哈希函数` md5、sha1 与 password_hash🔒

**解析**　`md5($s)` / `sha1($s)` 把字符串变成固定长度的摘要（分别是 32 / 40 位十六进制）。它们**不安全**：速度快、可被彩虹表撞库、`md5("0e...")` 还有魔法哈希问题——**存密码必须用 `password_hash()`**（自动加盐、慢哈希），校验用 `password_verify()`。

**操作**

```php
<?php
echo md5("123456") . "\n";
echo sha1("123456") . "\n";
$hash = password_hash("secret", PASSWORD_DEFAULT);
var_dump(password_verify("secret", $hash));
var_dump(password_verify("wrong", $hash));
echo "哈希长度：" . strlen($hash) . "\n";
// 运行结果：
// e10adc3949ba59abbe56e057f20f883e
// 7c4a8d09ca3762af61e59520943dc26494f8941b
// bool(true)
// bool(false)
// 哈希长度：60
```

> ⚠️ **渗透重点**：库里出现 32 位十六进制且是 `md5` 的，用 `hashcat -m 0` / 彩虹表几秒就破；`5f4dcc3b...` 就是 `123456` 的 md5。存密码**永远**用 `password_hash()`，比对用 `password_verify()`，别自己拼盐、别用 `==` 比哈希。

### `对称加密与随机数` openssl 加解密与随机数🔒

**解析**　`openssl_encrypt($数据, "aes-256-cbc", $密钥, 0, $iv)` 做对称加密（返回 base64 字符串），`openssl_decrypt` 解密；密钥长度要和算法匹配（AES-256 要 32 字节），IV 要 16 字节。随机数一律用 `random_bytes()` / `random_int()`，**不要用 `rand()`**。

**操作**

```php
<?php
$key = str_repeat("k", 32);            // 32 字节密钥（AES-256）
$iv = str_repeat("i", 16);             // 16 字节 IV
$enc = openssl_encrypt("secret message", "aes-256-cbc", $key, 0, $iv);
echo "密文：" . $enc . "\n";
echo "解密：" . openssl_decrypt($enc, "aes-256-cbc", $key, 0, $iv) . "\n";
echo "随机 16 字节的长度：" . strlen(random_bytes(16)) . "\n";
// 运行结果：
// 密文：IWuSSK862Gf9IyPnxU/EEw==
// 解密：secret message
// 随机 16 字节的长度：16
```

> ⚠️ `rand()`/`mt_rand()` **不是密码学安全的**：token、验证码、加密密钥必须用 `random_bytes()` 或 `random_int()`。IV 不要硬编码、要每次随机生成并随密文一起传；密钥别写死在代码里。

### `base64 编码解码` base64_encode 与 decode🔒

**解析**　`base64_encode($s)` 把二进制/字符串编成只含 `A-Za-z0-9+/=` 的可打印串，`base64_decode()` 还原。它不是加密（谁都能解），只是"换一种可安全传输的表示"。很多 webshell、payload 会做 base64 混淆。

**操作**

```php
<?php
$enc = base64_encode("hello 世界");
echo $enc . "\n";
echo base64_decode($enc) . "\n";
echo base64_decode("aGVsbG8=") . "\n";
// 运行结果：
// aGVsbG8g5LiW55WM
// hello 世界
// hello
```

> ⚠️ 看到代码里一堆 `base64_decode` 很可疑——这是最常见的**免杀/混淆**手法（webshell 把危险 payload 藏进 base64 字符串里）。审计时把可疑的 base64 串解出来看。

## 十四 危险函数（渗透必看）

### `system` 执行系统命令并直接输出🔒

**解析**　执行一条系统命令，并把结果**直接打印**到输出里（网页上也能看到）。这是渗透里拿到 webshell 后最常用的命令执行函数：`system($_GET["cmd"]);` 访问 `?cmd=id` 就能执行任意命令。

**操作**

```php
<?php
system("whoami");
echo "\n";
// 运行结果：
// zhangzixin
```

> ⚠️ 只要参数能被用户控制（`$_GET`/`$_POST`），就是**远程命令执行（RCE）**，服务器直接失守。

### `exec` 执行命令只返回最后一行🔒

**解析**　执行命令，**只返回最后一行输出**（不会自动打印）。第二个参数传一个变量，会把命令的**全部输出行**装进这个数组；第三个参数拿退出码。

**操作**

```php
<?php
$out = exec("whoami");
echo "最后一行：" . $out . "\n";
exec("printf 'a\nb\nc'", $lines);
print_r($lines);
// 运行结果：
// 最后一行：zhangzixin
// Array
// (
//     [0] => a
//     [1] => b
//     [2] => c
// )
```

> ⚠️ `exec` 不自动打印，常被 webshell 用来"悄悄"执行命令并把结果写文件/外带，比 `system` 更隐蔽。

### `shell_exec 与反引号` 执行命令返回全部输出🔒

**解析**　`shell_exec($cmd)` 执行命令，把**全部输出**当成一个字符串返回（不自动打印），通常配合 `echo` 显示。反引号 `` `cmd` `` 是 `shell_exec` 的简写。

**操作**

```php
<?php
$out = shell_exec("echo hello && whoami");
echo $out;
// 运行结果：
// hello
// zhangzixin
```

> ⚠️ 反引号 `` `cmd` `` 本来是 `shell_exec` 的简写，但 **PHP 8.5 起反引号运算符已被废弃**（本机实跑会报 `Deprecated: The backtick (`) operator is deprecated`），新代码统一用 `shell_exec()`。审计老代码时反引号仍是常见命令执行点。

### `passthru 与 popen` 其它命令执行函数🔒

**解析**　`passthru($cmd)` 执行并**原样输出**（适合二进制流）；`popen($cmd, "r")` 打开一个进程管道、用 `fread` 读输出、`pclose` 关闭；`proc_open()` 更底层、能控制输入输出和进程。它们全是命令执行点。

**操作**

```php
<?php
echo "passthru 直接输出：";
passthru("whoami");
$h = popen("echo 管道输出", "r");
echo "popen 读到：" . fread($h, 1024);
pclose($h);
// 运行结果：
// passthru 直接输出：zhangzixin
// popen 读到：管道输出
```

> ⚠️ `popen`/`proc_open` 能跑长期进程、双向通信，做反弹 shell 时常用；还有 `pcntl_exec`、`反引号`。做安全加固时把所有能起进程的函数都列进黑名单。

### `eval` 把字符串当代码执行🔒

**解析**　把一段**字符串当作 PHP 代码**运行：`eval("return 2+3;")` 得到 5。致命点：`eval($_POST["code"])` 等于让用户直接在服务器上写 PHP 代码——**代码执行（RCE）**，和拿到 shell 没区别。

**操作**

```php
<?php
$code = "2 + 3";
echo eval("return $code;") . "\n";
echo eval('return "动态" . "执行";') . "\n";
// 运行结果：
// 5
// 动态执行
```

> ⚠️ eval 进来的代码和主程序**共享变量作用域**，能读写当前所有变量。日常业务几乎不该用 eval；看到 `eval($_GET[...])` 或 `eval($_POST[...])` 基本可以确定是后门或漏洞。

### `assert` 断言（旧版可当代码执行）🔒

**解析**　`assert` 本意是"断言某条件为真"，用于调试。但 **PHP 7 及以前**，如果传进去的是字符串，它会把这串字符串**当 PHP 代码执行**——等价于 `eval`。

**操作**

```php
<?php
assert(1 === 1);
echo "断言通过\n";
var_dump((int) ini_get("zend.assertions"));   // 3=一直开 1=开发开 -1=关
echo "zend.assertions=" . ini_get("zend.assertions") . "\n";
// 运行结果：
// 断言通过
// int(1)
// zend.assertions=1
```

> ⚠️ 经典一句话木马就是 `assert($_POST["a"])`，在 PHP 5/7 上直接执行代码。**PHP 8 已取消对字符串参数的代码执行**，但大量老站点和 CTF 题目仍是这个环境。

### `unserialize` 反序列化字符串成对象🔒

**解析**　`serialize()` 把对象/数组变成字符串（便于存文件或传输），`unserialize()` 再还原成对象。安全用途：`unserialize($_GET["data"])` 时，攻击者能构造恶意序列化数据，触发对象里的魔术方法（`__wakeup`、`__destruct`、`__toString`），串成一条"**POP 链**"，最终执行代码。

**操作**

```php
<?php
class Demo {
    public $name = "test";
}
$data = serialize(new Demo());
echo $data . "\n";
$obj = unserialize($data);
echo $obj->name . "\n";
// 运行结果：
// O:4:"Demo":1:{s:4:"name";s:4:"test";}
// test
```

> ⚠️ **绝不反序列化用户输入**。实在要解析数据用 JSON（`json_decode`）。PHP 7 起可以传 `unserialize($data, ["allowed_classes" => false])` 只允许普通数据，但仍不如换成 JSON。

### `extract 与 parse_str` 变量覆盖漏洞🔒

**解析**　`parse_str("a=1&b=2", $arr)` 把查询串解析成数组；`extract($arr)` 把数组的键**直接变成当前作用域里的变量**。方便，但危险：如果 `extract($_GET)`，攻击者传参就能覆盖程序里的变量。

**操作**

```php
<?php
$params = "is_admin=1&user=guest&money=99999";
parse_str($params, $arr);
extract($arr);
echo "user=$user, is_admin=$is_admin, money=$money\n";
var_dump($is_admin === "1");
// 运行结果：
// user=guest, is_admin=1, money=99999
// bool(true)
```

> ⚠️ **变量覆盖漏洞根源**：`extract($_GET)`/`extract($_POST)` 等于让攻击者给任意变量赋值，常用来绕过 `if ($is_admin)` 这类判断。别对用户输入用 `extract`；`parse_str` 的第二个参数一定要给（不然会把变量直接倒进当前作用域）。

### `phpinfo` 信息泄露🔒

**解析**　`phpinfo()` 会把当前 PHP 的**全部配置、版本、已加载扩展、路径、环境变量**一次性打印成 HTML 页面。它对调试有用，但**绝不能留在生产环境**——等于把服务器底细白送给攻击者。

**操作**

```php
<?php
echo "PHP 版本：" . phpversion() . "\n";
echo "系统：" . php_uname("s") . " " . php_uname("m") . "\n";
echo "已加载扩展数：" . count(get_loaded_extensions()) . "\n";
echo "文档根目录：" . ($_SERVER["DOCUMENT_ROOT"] ?? "（CLI 下为空）") . "\n";
echo "提示：phpinfo() 会把以上信息以及全部配置、路径、环境变量打印成 HTML 页面。\n";
// 运行结果：
// PHP 版本：8.5.11
// 系统：Darwin arm64
// 已加载扩展数：66
// 文档根目录：
// 提示：phpinfo() 会把以上信息以及全部配置、路径、环境变量打印成 HTML 页面。
```

> ⚠️ 渗透第一步常是找 `phpinfo.php`/`info.php`/`test.php` 这类探针文件（或 `?phpinfo=1` 参数）。防御：删掉、或用 `disable_functions`/限 IP 访问。

### `危险函数与超全局变量` 拼接就是漏洞🔒

**解析**　把前面串起来：只要"用户能控制的输入"（`$_GET`/`$_POST`/`$_COOKIE`/`$_REQUEST`/`$_FILES` 里的值）**直接拼进**上面那些危险函数，攻击者就能改写程序行为——命令执行、代码执行、文件读取、SQL 注入。问题不在某个函数，而在于**把"数据"当成"代码/命令/结构"来用**。

**操作**

```php
<?php
// ❌ 这些都是漏洞写法（此处仅注释示意，不在本机执行）：
// system($_GET["cmd"]);        // ?cmd=id          → 命令执行（RCE）
// eval($_POST["code"]);        // 提交任意 PHP 代码 → 代码执行
// include($_GET["page"]);      // ?page=/etc/passwd → 任意文件读取（LFI）
// $pdo->query("... WHERE id=" . $_GET["id"]);        → SQL 注入

// ✅ 正确思路：白名单 / 参数化 / 转义，绝不让用户输入决定"执行什么"
$allow = ["home", "about"];
$page = in_array($_GET["page"] ?? "", $allow, true) ? $_GET["page"] : "home";
echo "允许的页面：" . $page . "\n";
// 运行结果：
// 允许的页面：home
```

> ⚠️ 防御总原则：命令用白名单或 `escapeshellarg()`；SQL 用参数化查询；包含文件用白名单；输出到页面前用 `htmlspecialchars()` 防 XSS。**永远别让用户输入决定"执行什么"。**
