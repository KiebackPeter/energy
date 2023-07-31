# Import all the models, so that Base has them before being
# imported by Alembic in order
from .base_model import BaseModel # pylint: disable=unused-import

from .user import UserModel  # pylint: disable=unused-import
from .installation import InstallationModel  # pylint: disable=unused-import
from .meter import MeterModel  # pylint: disable=unused-import
from .channel import ChannelModel  # pylint: disable=unused-import
from .measurement import MeasurementModel  # pylint: disable=unused-import
