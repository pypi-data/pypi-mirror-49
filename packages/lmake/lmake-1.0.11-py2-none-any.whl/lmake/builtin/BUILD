shell_script(name = "protobuf",
             script = "install_protobuf.py",
             export = 'libprotobuf.a',
             export_bin = { 'PROTOC': '.build/.lib/m${PLATFORM}/bin/protoc' }
             )

shell_script(name = "lua",
             script = "install_lua.py",
             export = 'liblua.a',
             )

shell_script(name = "libuv",
             script = "install_libuv.py",
             export = 'libuv_a.a',
             )

shell_script(name = "cassandra",
             script = "install_cassandra.py",
             export = 'libcassandra_static.a',
             deps = [
                      ":libuv"
                    ]
             )

shell_script(name = "avro",
             script = "install_avro.py",
             export = 'libavrocpp_s.a',
             )

shell_script(name = "jsoncpp",
             script = "install_jsoncpp.py",
             export = "libjsoncpp.a",
             )

shell_script(name = "pci",
             script = "install_pciutils.py",
             export = "libpci.a",
             )

