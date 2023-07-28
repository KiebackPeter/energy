from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, select, insert
from sqlalchemy.exc import IntegrityError
from app.database.models.measurement import MeasurementModel
from app.schemas.measurements import MeasurementCreateDTO, MeasurementPublic
from app.core.implementations.base_crud import Session, CRUDBase # ,log

# NOTE: accumulated values come from sql trigger.
# FIXME: cannot create many for the same channel


class CRUDMeasurement(
    CRUDBase[MeasurementModel, MeasurementCreateDTO, MeasurementPublic]
):
    def create(
        self, session: Session, create_obj: MeasurementCreateDTO, channel_id: int
    ) -> MeasurementModel:
        measurement_data = jsonable_encoder(create_obj)
        measurement_data["channel_id"] = channel_id
        return session.scalars(
            insert(self.model).values(measurement_data)
        ).one()
        # TODO: catch constain on double timestamps for a channel_id
        # try:
        #     self.refresh(session, database_model=measurement)
        # except IntegrityError as err:
        #     log.critical("already have this timestamp for channel_id: %s", err.params)
        # return measurement

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

    def latest_measurement(
        self, session: Session,
        channel_id: int
    ):

        measurement = session.scalars(
            select(self.model.timestamp)
            .filter_by(channel_id = channel_id)
            .order_by(desc(self.model.timestamp))
        ).one_or_none()

        print(f"lastest channel {measurement}")
        if measurement:
                return datetime.fromtimestamp(measurement)
        else:
            return datetime.today() - timedelta(days=(365 * 5))

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
