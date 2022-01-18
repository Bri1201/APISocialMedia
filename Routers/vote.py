import fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
import oAuth2, Model, schemas, database

router = APIRouter(prefix="/votes", tags=['Votes'])

#Model.Base.metadata.create_all(bind=engine)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votec: schemas.Vote, db: session = Depends(database.get_db),
         current_user: int = Depends(oAuth2.get_current_user)):
    post = db.query(Model.Post).filter(Model.Post.id == votec.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {votec.post_id} not found")
    vote_query = db.query(Model.Vote).filter(Model.Vote.post_id == votec.post_id, Model.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (votec.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {votec.post_id}")
        new_vote = Model.Vote(post_id=votec.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}
    elif (votec.dir == 0):
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Vote deleted"}
