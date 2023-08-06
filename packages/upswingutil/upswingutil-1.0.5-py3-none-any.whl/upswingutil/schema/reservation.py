from typing import Optional
from typing import List
from upswingutil.schema import Token, Alvie
from pydantic import BaseModel


class PropertyInfo(BaseModel):
    hotelId: str
    clientId: str
    orgId: str
    agent: str
    hotelName: str
    numberOfRooms: int
    roomId: str
    roomName: str
    roomType: str
    roomClass: str
    roomTypeCharged: str
    roomNumberLocked: bool
    pseudoRoom: bool


class TravelType(BaseModel):
    id: int
    name: str
    type: str
    score: float
    addedBy: str


class GuestProfile(BaseModel):
    guestId: str
    firstName: Optional[str] = ''
    middleName: Optional[str] = ''
    lastName: Optional[str] = ''
    primary: Optional[bool] = False
    address: Optional[dict]
    profileType: Optional[str] = ''
    primary: Optional[bool] = False
    arrivalTransport: Optional[dict]
    departureTransport: Optional[dict]


class GuestInfo(BaseModel):
    adultCount: int
    childrenCount: int
    infantCount: int
    guest_list: List[GuestProfile]


class BookingChannelInfo(BaseModel):
    saleSourceType: str
    saleSourceCode: str
    sourceCode: str
    sourceDescription: str
    channelCode: str
    bookingMedium: Optional[str] = ''
    bookingMediumDescription: Optional[str] = ''


class BookingFinancialInfo(BaseModel):
    class RoomRate(BaseModel):
        start: str
        end: str
        total: dict
        rates: dict
        guestCounts: dict
        suppressRate: bool = False
        houseUseOnly: bool = False
        complimentary: bool = False
        discountAllowed: bool = False
        bogoDiscount: bool = False

    currencyCode: str
    rateAmount: float
    paymentMethod: str
    fixedRate: Optional[bool]
    rateSuppressed: Optional[bool]
    ratePlanCode: Optional[str]
    total: Optional[dict]
    roomRates: Optional[List[RoomRate]] = []


class Reservation(BaseModel):
    id: str
    idObj: dict
    orgId: str
    agent: str
    hotelId: str
    hotelName: str
    globalId: str
    status: str
    alerts: list
    financeInfo: dict
    guestInfo: dict
    arrivalDate: str
    departureDate: str
    expectedTimes: dict
    bookingInfo: dict
    token: Optional[Token] = None
    roomStay: Optional[dict] = None
    originalTimeSpan: Optional[dict] = None
    callHistory: Optional[list] = []
    cancellation: Optional[list] = []
    comments: Optional[list] = []
    createBusinessDate: Optional[str] = ''
    createDateTime: Optional[str] = ''
    guestLocators: Optional[dict]
    policies: Optional[dict] = None
    inventoryItems: Optional[dict] = None
    linkedReservation: Optional[dict] = None
    preferences: Optional[list] = []
    metaInfo: dict
    daily_activity: Optional[list] = []
    eCertificates: Optional[list] = []
    memberships: Optional[list] = []
    packages: Optional[list] = []
    folioInformation: Optional[dict] = None
    alvie: Optional[Alvie] = Alvie()


if __name__ == '__main__':
    # reservation = Reservation(
    #     resvId="001",
    #     agent="ORACLE",
    #     arrivalDate="2021-01-01",
    #     departureDate="2021-01-10",
    #     reservationStatus='NoShow',
    #     propertyInfo={
    #         'hotelId': 'SAN01',
    #         'orgId': 'OHILP',
    #         'clientId': 'SAN01',
    #         'agent': 'ORACLE',
    #         'hotelName': 'OHIP Sandbox 1',
    #         'numberOfRooms': 1,
    #         'roomId': '001',
    #         'roomName': '001',
    #         'roomType': 'DBL',
    #         'roomClass': 'STD',
    #         'roomTypeCharged': 'DBL',
    #         'roomNumberLocked': False,
    #         'pseudoRoom':  False
    #     },
    #     travel_type=[
    #         {
    #             'id': 1,
    #             'name': 'Business',
    #             'score': 1,
    #             'addedBy': 'ALVIE'
    #         }
    #     ],
    #     originalTimeStamp={
    #         'startDate': '2021-01-21',
    #         'endDate': '2021-01-31'
    #     },
    #     channelInfo={
    #         'bookingSourceType': '',
    #         'bookingSourceCode': '',
    #         'bookingChannelCode': ''
    #     },
    #     financialInfo={
    #         'currencyCode': 'USD',
    #         'rateAmount': 200,
    #         'paymentMethod': 'CA',
    #         'fixedRate': True,
    #         'rateSuppressed': False,
    #         'ratePlanCode': 'SDF'
    #     },
    #     guestInfo={
    #         'adultCount': 1,
    #         'childrenCount': 1,
    #         'infantCount': 1,
    #         'guest_list': [
    #             {
    #                 'guestId': '0002123',
    #                 'firstName': 'Harsh',
    #                 'lastName': 'Mathur',
    #                 'language': 'E',
    #             }
    #         ]
    #     }
    # )
    g = GuestProfile(
        guestId=123,
        firstName=None
    )
    print(g.json())
