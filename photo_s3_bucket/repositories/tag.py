from sqlalchemy.orm import Session

from photo_s3_bucket.models.tag import Tag

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, path: str, tag: str) -> Tag:
        tag_obj = Tag(path=path, tag=tag)
        self.session.add(tag_obj)
        self.session.commit()
        return tag_obj

    def get_by_path(self, path: str) -> list[Tag]:
        return self.session.query(Tag).filter_by(path=path)
    
    def get_by_tag(self, tag: str) -> list[Tag]:
        return self.session.query(Tag).filter_by(tag=tag)

    def get_by_path_and_tag(self, path: str, tag: str) -> Tag:
        return self.session.query(Tag).filter_by(path=path, tag=tag).first()


    def delete(self, path: str, tag: str) -> bool:
        tag_obj = self.get_by_path_and_tag(path, tag)
        if tag_obj:
            self.session.delete(tag_obj)
            self.session.commit()
            return True
        return False
