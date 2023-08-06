from typing import Optional

from hypothesis import strategies
from sqlalchemy.sql.sqltypes import (BigInteger,
                                     Boolean,
                                     Date,
                                     DateTime,
                                     Enum,
                                     Float,
                                     Integer,
                                     Interval,
                                     LargeBinary,
                                     SmallInteger,
                                     String,
                                     Time)
from sqlalchemy.sql.type_api import TypeEngine

from hypothesis_sqlalchemy import enumerable
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import sql_identifiers


def strings_factory(lengths: Strategy[int] =
                    strategies.integers(min_value=0,
                                        # Postgres VARCHAR max size
                                        max_value=10485760)
                    ) -> Strategy[TypeEngine]:
    return strategies.builds(String,
                             length=lengths)


def binary_strings_factory(lengths: Strategy[int] =
                           strategies.integers(min_value=0,
                                               # MySQL BLOB max size
                                               max_value=65535)
                           ) -> Strategy[TypeEngine]:
    return strategies.builds(LargeBinary,
                             length=lengths)


def primary_keys_factory() -> Strategy[TypeEngine]:
    types = [SmallInteger, Integer, BigInteger]
    return strategies.one_of(*map(strategies.builds, types))


def enums_factory(*,
                  values: Strategy[str] = sql_identifiers,
                  min_size: int = 1,
                  max_size: Optional[int] = None) -> Strategy[TypeEngine]:
    enums_keys = values.filter(enumerable.is_valid_key)
    return ((strategies.tuples(enumerable.factory(keys=enums_keys,
                                                  min_size=min_size,
                                                  max_size=max_size))
             | strategies.lists(values,
                                min_size=min_size,
                                max_size=max_size))
            .map(lambda type_values: Enum(*type_values)))


def factory(*,
            string_types: Strategy[TypeEngine] = strings_factory(),
            binary_string_types: Strategy[TypeEngine] =
            binary_strings_factory(),
            enum_types: Strategy[TypeEngine] = enums_factory(),
            primary_keys_types: Strategy[TypeEngine] = primary_keys_factory()
            ) -> Strategy[TypeEngine]:
    extra_types = [Float(asdecimal=True), Boolean(),
                   Date(), DateTime(), Interval(), Time()]
    return strategies.one_of(string_types,
                             binary_string_types,
                             enum_types,
                             primary_keys_types,
                             strategies.sampled_from(extra_types))
