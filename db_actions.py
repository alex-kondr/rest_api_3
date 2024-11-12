from db import Post, Session


def add_post(author, text):
    with Session() as session:
        post = Post(author=author, text=text)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post.id


def get_posts():
    with Session() as session:
        return session.query(Post).all()


def get_post(id):
    with Session() as session:
        return session.query(Post).where(Post.id == id).first()


def update_post(id, author, text):
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        post.author = author
        post.text = text
        session.commit()
        return "Статтю успішно оновлено"


def delete_post(id):
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        session.delete(post)
        session.commit()
        return "Статтю успішно видалено"
