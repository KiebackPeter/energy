# Import all the models, so that Base has them before being
# imported by Alembic in order
from app.core.implementations.base_model import BaseModel  # type: ignore # pylint: disable=unused-import

from .user import UserModel  # type: ignore # pylint: disable=unused-import disable=relative-beyond-top-level
from .installation import InstallationModel  # type: ignore  # pylint: disable=unused-import disable=relative-beyond-top-level
from .meter import MeterModel  # type: ignore # pylint: disable=unused-import disable=relative-beyond-top-level
from .channel import ChannelModel  # type: ignore # pylint: disable=unused-import disable=relative-beyond-top-level
from .measurement import MeasurementModel  # type: ignore # pylint: disable=unused-import disable=relative-beyond-top-level
