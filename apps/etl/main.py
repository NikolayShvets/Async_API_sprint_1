import time
from utils import get_postges_connection, logger
from state import State, JsonFileStorage
from settings import settings
from producer import PostgresProducer
from enricher import PostgresEnricher
from merger import PostgresMerger
from transformer import Transformer
from loader import ElasticsearchLoader


def main():
    logger.info('etl process started')
    with get_postges_connection() as conn:
        state = State(storage=JsonFileStorage(file_path=settings['storage_file_path']))
        producer = PostgresProducer(conn=conn, extract_size=settings['etl_extract_size'])
        enricher = PostgresEnricher(conn=conn)
        merger = PostgresMerger(conn=conn)
        transformer = Transformer()
        loader = ElasticsearchLoader(host=settings['elastic_host'], port=settings['elastic_port'])

        while True:
            filmwork_updates = producer.check_filmwork_updates(
                last_updated_time=state.get_state('movie_modified') or settings['etl_start_time']
            )

            for updated_table, updated_entities, modified in filmwork_updates:
                index_name = 'movies'
                enriched_entities = enricher.enrich(table=updated_table, entity_ids=updated_entities)
                merged_entities = merger.merge(enriched_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_movie_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f'{index_name}_modified', value=modified.strftime('%Y-%m-%d %H:%M:%S.%f %z'))

                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings['etl_iteration_sleep_time']} seconds"
                )
                time.sleep(settings['etl_iteration_sleep_time'])

            person_updates = producer.check_person_updates(
                last_updated_time=state.get_state('person_modified') or settings['etl_start_time']
            )

            for updated_entities, modified in person_updates:
                index_name = 'persons'
                merged_entities = merger.merge(updated_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_person_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f'{index_name}_modified', value=modified.strftime('%Y-%m-%d %H:%M:%S.%f %z'))
                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings['etl_iteration_sleep_time']} seconds"
                )
                time.sleep(settings['etl_iteration_sleep_time'])

            genre_updates = producer.check_genre_updates(
                last_updated_time=state.get_state('genre_modified') or settings['etl_start_time']
            )

            for updated_entities, modified in genre_updates:
                index_name = 'genres'
                merged_entities = merger.merge(updated_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_genre_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f'{index_name}_modified', value=modified.strftime('%Y-%m-%d %H:%M:%S.%f %z'))
                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings['etl_iteration_sleep_time']} seconds"
                )
                time.sleep(settings['etl_iteration_sleep_time'])

            logger.info(f"no updates found, slepping {settings['etl_checking_updates_sleep_time']} seconds")
            time.sleep(settings['etl_checking_updates_sleep_time'])


if __name__ == '__main__':
    main()
