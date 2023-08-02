from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.database.models.measurement import MeasurementModel
from app.schemas.measurements import MeasurementCreateDTO, MeasurementPublic
from app.database.crud.base_crud  import Session, CRUDBase, select, insert, desc  # , log,


class CRUDMeasurement(
    CRUDBase[MeasurementModel, MeasurementCreateDTO, MeasurementPublic]
):
    def create(
        self, session: Session, create_obj: MeasurementCreateDTO, channel_id: int
    ) -> MeasurementModel:
        measurement_data = jsonable_encoder(create_obj)
        measurement_data["channel_id"] = channel_id
        return session.scalar(
            insert(self.model).values(measurement_data)
        )

    def get_with_date_range(
        self,
        session: Session,
        *,
        channel_id: int,
        from_date: float,
        till_date: float,
    ):
        """Returns a list of measurements for a channel with given from and till dates"""
        return (
            session.query(self.model)
            .filter(
                self.model.timestamp.between(from_date, till_date),
                self.model.channel_id == channel_id,
            )
            .all()
        )

    def latest_channel_measurement(self, session: Session, channel_id: int) -> datetime:
        measurement = session.scalars(
            select(self.model)
            .filter_by(channel_id=channel_id)
            .order_by(desc(self.model.timestamp))
        ).first()
        if measurement:
            return datetime.fromtimestamp(measurement.timestamp)

    def delete_since(
        self,
        session: Session,
        channel_id: int,
        from_date: float,
    ):
        session.query(self.model).filter(
            self.model.channel_id == channel_id,
            self.model.timestamp > from_date,
        ).delete()
        session.commit()

        return f"succesfully deleted {from_date} for channel: {channel_id}"


measurement_crud = CRUDMeasurement(MeasurementModel)
