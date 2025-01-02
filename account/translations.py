TRANSLATIONS = {
    "Bad Request": "درخواست نامعتبر",
    "Username": "نام کاربری",
    "Password": "رمز عبور",
    "OTP sent": "رمز یکبار مصرف ارسال شد",
    "OTP sent to your email address. Please verify OTP to proceed.":
        "رمز یکبار مصرف به آدرس ایمیل شما ارسال شد. لطفاً برای ادامه، رمز را تأیید کنید.",
    "Unauthorized": "غیرمجاز",
    "Please provide both username and password.": "لطفاً هر دو نام کاربری و رمز عبور را وارد کنید.",
    "Ciz-Miz Login OTP": "رمز یکبار مصرف ورود سیز-میز",
    "Your OTP for login is: %(otp)s": "رمز یکبار مصرف شما برای ورود: %(otp)s",
    "Invalid credentials": "اطلاعات ورود نامعتبر است",
    "OTP": "رمز یکبار مصرف",
    "Login successful": "ورود موفقیت‌آمیز بود",
    "Invalid or expired OTP": "رمز یکبار مصرف نامعتبر یا منقضی شده است",
    "User not found": "کاربر یافت نشد",
    "Please provide both username and OTP.": "لطفاً هر دو نام کاربری و رمز یکبار مصرف را وارد کنید.",
    "Invalid or expired OTP.": "رمز یکبار مصرف نامعتبر یا منقضی شده است.",
    "User not found.": "کاربر یافت نشد.",
    "Logout successful": "خروج موفقیت‌آمیز بود",
}

def translate(key, **kwargs):
    """
    Translates the given key using the TRANSLATIONS dictionary.
    Allows for optional placeholders like %(otp)s to be filled in using kwargs.

    Args:
        key (str): The key to translate.
        kwargs: Keyword arguments to format placeholders in the translation.

    Returns:
        str: The translated string or the original key if translation is not found.
    """
    template = TRANSLATIONS.get(key, key)
    return template % kwargs if kwargs else template