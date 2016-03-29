from core.api import API


class Status(object):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    KILLED = "KILLED"

    @staticmethod
    def get(_id: str) -> int:
        result = API.db.jobs.find_one(
            {'_id': _id}
        )

        if result:
            return result['status']

    @staticmethod
    def set(_id: str, status: str) -> None:  # TODO: Annotate status
        if API.db is not None:
            API.db.jobs.update_one(
                {
                    '_id': _id
                },
                {
                    '$set': {'status': status}
                }
            )
        else:
            client = API.create_mongo()
            db = client.dune

            db.jobs.update_one(
                {
                    '_id': _id
                },
                {
                    '$set': {'status': status}
                }
            )

            client.close()
