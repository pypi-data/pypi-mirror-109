# Copyright (c) 2021, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from datetime import datetime, timedelta
import random
from cerebralcortex.core.datatypes import DataStream
from cerebralcortex.core.metadata_manager.stream.metadata import Metadata, DataDescriptor, ModuleMetadata
from cerebralcortex.core.util.spark_helper import get_or_create_sc

def gen_accel_gyro_data(CC, study_name, user_id, stream_name, version=1, hours=1, frequency=32):
    """
    Create pyspark dataframe with some sample phone battery data
    Returns:
        DataFrame: pyspark dataframe object with columns: ["timestamp", "battery_level", "version", "user"]

    """
    column_name = ["timestamp", "localtime", "user" ,"version", "x", "y", "z"]
    sample_data = []
    timestamp = datetime(2019, 1, 9, 11, 34, 59)

    sqlContext = get_or_create_sc("sqlContext")
    total_hours = (hours*60*60)*frequency
    for row in range(total_hours):
        x = round(random.uniform(-2,2),8)
        y = round(random.uniform(-2,2),8)
        z = round(random.uniform(-2,2),8)
        timestamp = timestamp + timedelta(milliseconds=1)
        localtime = timestamp - timedelta(hours=5)
        sample_data.append((timestamp, localtime, user_id, version, x, y, z))
    df = sqlContext.createDataFrame(sample_data, column_name)

    stream_metadata = Metadata()
    stream_metadata.set_study_name(study_name).set_name(stream_name).set_description("wrist watch sensor sample data stream.") \
        .add_dataDescriptor(
        DataDescriptor().set_name("timestamp").set_type("datetime").set_attribute("description", "UTC timestamp of data point collection.")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("localtime").set_type("datetime").set_attribute("description", "local timestamp of data point collection.")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("user").set_type("string").set_attribute("description", "user id")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("version").set_type("int").set_attribute("description", "version of the data")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("x").set_type("float").set_attribute("description", "x-axis")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("y").set_type("float").set_attribute("description", "y-axis")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("z").set_type("float").set_attribute("description", "z-axis")) \
        .add_module(
        ModuleMetadata().set_name("phone.sensors").set_version("1.2.4").set_attribute("attribute_key", "attribute_value").set_author(
            "Nasir Ali", "software@md2k.org"))
    stream_metadata.is_valid()

    ds = DataStream(df, stream_metadata)
    CC.save_stream(ds)


