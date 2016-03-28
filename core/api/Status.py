from core.api import API


class Status(object):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    KILLED = "KILLED"

    @staticmethod
    def get(_id: str) -> int:
        result = API.mongo_client.db.jobs.find_one(
            {'_id': _id}
        )

        if result:
            return result['status']

    @staticmethod
    def set(_id: str, status: str) -> None: # TODO: Annotate status
        API.mongo_client.db.jobs.update_one(
            {
                '_id': _id
            },
            {
                '$set': {'status': status}
            }
        )
