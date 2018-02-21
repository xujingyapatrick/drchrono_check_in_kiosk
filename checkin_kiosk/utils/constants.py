
class AppointmentStatus():
    EMPTY = ""
    ARRIVED = "Arrived"
    CHECKED_IN = "Checked In"
    IN_ROOM = "In Room"
    CANCELLED = "Cancelled"
    COMPLETE = "Complete"
    CONFIRMED = "Confirmed"
    IN_SESSION = "In Session"
    NO_SHOW = "No Show"
    NOT_CONFIRMED = "Not Confirmed"
    RESCHEDULED = "Rescheduled"
    STATUS = ("", "Arrived", "Checked In", "In Room", "Cancelled", "Complete", "Confirmed", "In Session", "No Show",
              "Not Confirmed", "Rescheduled")


    @classmethod
    def is_valid_status(cls, status):
        return status in cls.STATUS


class Gender():
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

class Ethnicity():
    BLANK = 'blank'
    HISPANIC = "hispanic"
    NOT_HISPANIC = "not_hispanic"
    DECLINED = "declined"

class Race():
    BLANK = "blank"
    INDIAN = "indian"
    ASIAN = "asian"
    BLACK = "black"
    HAWAIIAN = "hawaiian"
    WHITE = "white"
    DECLINED= "declined"