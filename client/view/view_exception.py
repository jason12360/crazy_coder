class UsrnameOrPasswdBlankException(Exception):
    pass


class UsrnameOrPasswdNotExistException(Exception):
    pass


class UsrnameOrPasswdAlreadyExistException(Exception):
    pass


class UsrnameNotMeetRequirements(Exception):
    pass


class PasswdNotMeetRequirements(Exception):
    pass


class ConfirmedPasswdNotMatch(Exception):
    pass
