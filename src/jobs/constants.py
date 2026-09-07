class CacheKeys:
    CATEGORY_LIST = 'taskflow:categories:list'
    CATEGORY_DETAIL_PATTERN = 'taskflow:categories:detail:{}'
    JOB_LIST_PATTERN = 'taskflow:jobs:list:{}'
    JOB_DETAIL_PATTERN = 'taskflow:jobs:detail:{}'

    @classmethod
    def get_category_list_key(cls) -> str:
        return cls.CATEGORY_LIST

    @classmethod
    def get_category_detail_key(cls, category_id: int) -> str:
        return cls.CATEGORY_DETAIL_PATTERN.format(category_id)

    @classmethod
    def get_job_list_key(cls, user_id: int) -> str:
        return cls.JOB_LIST_PATTERN.format(user_id)

    @classmethod
    def get_job_detail_key(cls, job_id: int) -> str:
        return cls.JOB_DETAIL_PATTERN.format(job_id)
