from sqlalchemy.orm import Session

from photo_s3_bucket.models.rate import Rate


class RateRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, path: str, rate: int) -> Rate:
        rate_obj = Rate(path=path, rate=rate)
        self.session.add(rate_obj)
        self.session.commit()
        return rate_obj

    def get_by_path(self, path: str) -> Rate:
        return self.session.query(Rate).filter_by(path=path).first()

    def update_rate(self, path: str, new_rate: int) -> Rate:
        rate_obj = self.get_by_path(path)
        if rate_obj:
            rate_obj.rate = new_rate
            self.session.commit()
        return rate_obj

    def create_or_update(self, path: str, rate: int) -> Rate:
        rate_obj = self.get_by_path(path)
        if rate_obj:
            return self.update_rate(path, rate)
        return self.create(path, rate)

    def delete(self, path: str) -> bool:
        rate_obj = self.get_by_path(path)
        if rate_obj:
            self.session.delete(rate_obj)
            self.session.commit()
            return True
        return False
