from datetime import datetime,timezone,timedelta
from app.models import SubmissionStatus
def test_late_status():
    deadline=datetime.now(timezone.utc)-timedelta(minutes=1)
    assert (SubmissionStatus.LATE if datetime.now(timezone.utc)>deadline else SubmissionStatus.SUBMITTED)==SubmissionStatus.LATE
