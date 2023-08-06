# Biliget ģ�鵵��
## ��װ
��cmd�������������װ

    pip install biliget
    python3 -m pip install biliget


�����ṩ������  basics,fun,ob

��python�����У���Ҫ��������

    from biliget import basics
	from biliget import fun
	from biliget import ob

--------------------------------
# ģ�����
### basics �������Ϊ������

| ����  | ��Ч  |
| :-: | :-: |
| Videoget( aid )  | ��Ƶ��Ϣ����  |
| Userget( uid ) | �û���Ϣ���� |

### ���Ƿ�����

#### Videoget( aid )��

| ����  | �ص�  | �������� |
| :------------: | :------------: |  :------------: |
| id()  | �û�id  | int |
| view()  | �ۿ���  | int |
| dan() | ��Ļ��  | int |
| reply() | ������  | int |
| favorite()  | �ղ���  | int |
| coin()  | Ӳ����  | int |
| share()  | ������  | int |
| like()  | ������  | int |
| copyright()  | ��Ȩ״̬  |int|
| detail()  | ��ϸ��Ϣ  |json|
| ownerid()  | ��Ƶ����id  |int|
| title()  |  ��Ƶ���� |str|
| cover()  | ��Ƶ����url  |str|
| desc() |  ��Ƶ���  |str|

#### Userget( uid ):

| ����  | �ص�  | �������� |
| :------------: | :------------: | :------------: |
| userinfo()  | �û�һ����Ϣ  | json  |
|  id() | �û�uid  | int  |
| following()  | �û���ע��  | int  |
| whisper()  | �û�˽�������޷���ȡ��  | int  |
| black()  | �û��������� ���޷���ȡ�� |  int |
| follower()  | �û���˿��  |  int |
|  upinfo() | �û�������Ϣ  | json  |
| username()  | �û���  | str  |
| sex()  |  �û��Ա� ��orŮ | str  |
| face()  | �û�ͷ������  | str  |
| sign()  | �û�����ǩ��  | str  |
| level()  | �û��ȼ�  | int  |
| birthday()  | �û����� mm-dd  | str  |
| badge()  | �û��Ƿ��Լ��ķ�˿ѫ��  | bool  |
| intr()  | �û�����֤��Ϣ  | str  |
| viptype()  | �û�vip��� 0:��  1:��ͨVIP 2:���VIP| int  |
| vipthemetype()  |  vip����״̬ | bool  |
| isfollowed()  | �Ƿ���Ա�ֱ�ӹ�ע  | bool  |
| toppic()  |  ��ҳ����ͼƬurl | str  |
| liveinfo()  | ֱ����Ϣ����  |  json |
| liveurl()  | ֱ��������  | str  |
| liveroomid()  |  ֱ����� |  int |
| liveroomcover()  |ֱ�����������   | str  |
| uservideoinfo()  | �û���Ƶ��ǩ  |  list |
| usertags()  | ��Ƶҳ����Ϣ  | json  |
| newv()  |   �û�������Ƶid | int  |


--------------------------------

### fun�������һ����

| ����  | ��Ч  |
| :-: | :-: |
| Ds()| ��ȡ��վĬ���������� |

#### �������·���

| ����  | �ص�  | �������� |
| :------------: | :------------: |  :------------: |
| showname()  | ������������������  | str |
| dstype()  | ����ָ��ҳ������ 1Ϊ��Ƶ  | int |
| value() | �ж����Ͳ�����ֵ$^1$  | list |
| url() | ����ָ��url  | str |
| all()  | ����Ĭ����������������  | json |

1:  
 ���Ϊ��Ƶ�� ['video',aid] || aid->int
 

 ���Ϊ������ ['other',...]

--------------------------------


### ob�������2����

| ����  | ��Ч  |
| :-: | :-: |
| Fanslook(pagesize)^2 | ��ȡ���ֵ�ù�ע��up�� |
| Bilitime() | bilibili����������Ϣ |


2��
pagesize��������ֵ����������ѡ��Ĭ��ֵΪ5 (������ֵ)

#### ���������·���

## Fanslook():

| ����  | �ص�  | �������� |
| :------------: | :------------: |  :------------: |
| fans()  | ��ȡ���ֵ�ù�ע��up����˿���Լ�uid  | list |
|____copyright____()  | ��Ȩ˵��  | print() |

#### fans()�ķ���ֵ

    [['��ξ�', 102885422, -6150], ... ]
    
    #����һ��list�������list�Ľṹ
    #�ڲ�list�Ľṹ�� ��һ��-up����  �ڶ���-up��uid  ������-��˿�仯
    #���Է���5��

## Bilitime():

| ����  | �ص�  | �������� |
| :------------: | :------------: |  :------------: |
| draw()  |  matplotlib������ͼ  | none |
| zipped()  | ��Ϣ����  | list |


#### zipped()�ķ���ֵ

    [[6403023, 4859422, '2019-07-13 12:23:44'], ... ]

    #����һ��list�������list�Ľṹ
    #�ڲ�list�Ľṹ�� ��һ��-���߲�����  �ڶ���-��������  ������-ʱ��
    #���Է���24��