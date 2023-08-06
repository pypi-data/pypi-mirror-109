from .utils import is_mykad_valid


class MyKad:
    """The base MyKad class.

    :param mykad_num: The MyKad number. This can contain numbers and '-'
    :type mykad_num: str, int
    """
    def __init__(self, mykad_num):
        if (is_mykad_valid(mykad_num)):
            self.mykad_num = mykad_num
        else:
            raise ValueError('MyKad number is not valid')

        # If MyKad is valid we should extract the information out of it
        # YYMMDD-PB-###G
        self.birth_year_num = self.mykad_num[0:2]
        self.birth_month_num = self.mykad_num[2:4]
        self.birth_day_num = self.mykad_num[4:6]
        self.birthplace_num = self.mykad_num[6:8]
        self.nrd_num = self.mykad_num[8:11]
        self.gender_num = self.mykad_num[-1]

    def get_unformatted(self):
        """Returns the unformatted MyKad string (i.e. just numbers, without '-')

        :return: The unformatted MyKad number
        :rtype: str
        """
        return self.mykad_num.replace('-', '')

    def get_formatted(self):
        """Returns the formatted MyKad string (with '-')

        :return: The formatted MyKad number
        :rtype: str
        """
        return f'{self.birth_year_num}{self.birth_month_num}{self.birth_day_num}-{self.birthplace_num}-{self.nrd_num}{self.gender_num}'

    def get_birth_year(self):
        """Returns the birth year of the MyKad holder.

        :return: The birth year in YYYY format
        :rtype: str
        """

        # MyKads started being issued in the year 1949
        if int(self.birth_year_num) >= 49:
            return f'19{self.birth_year_num}'

        return f'20{self.birth_year_num}'

    def get_birth_month(self):
        """Returns the birth month of the MyKad holder.

        :return A birth month in English
        :rtype str
        """

        month_dict = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        }

        return month_dict[self.birth_month_num]

    def is_male(self):
        return int(self.gender_num) % 2 != 0

    def is_female(self):
        return int(self.gender_num) % 2 == 0

    def get_gender(self):
        """Returns the gender of the MyKad holder.

        :return Either "Male" or "Female"
        :rtype str
        """

        if self.is_male():
            return "Male"
        else:
            return "Female"
