package(default_visibility = ["//visibility:public"])

load(
    "@io_bazel_rules_go//go:def.bzl",
    "go_binary",
    "go_library",
    "go_test",
)

go_binary(
    name = "transform",
    importpath = "k8s.io/test-infra/velodrome/transform",
    library = ":go_default_library",
)

go_test(
    name = "go_default_test",
    srcs = [
        "fetcher_test.go",
        "influx_test.go",
    ],
    importpath = "k8s.io/test-infra/velodrome/transform",
    library = ":go_default_library",
    deps = [
        "//velodrome/sql:go_default_library",
        "//velodrome/sql/testing:go_default_library",
    ],
)

go_library(
    name = "go_default_library",
    srcs = [
        "fetcher.go",
        "influx.go",
        "transform.go",
    ],
    importpath = "k8s.io/test-infra/velodrome/transform",
    deps = [
        "//velodrome/sql:go_default_library",
        "//velodrome/transform/plugins:go_default_library",
        "//vendor/github.com/golang/glog:go_default_library",
        "//vendor/github.com/influxdata/influxdb/client/v2:go_default_library",
        "//vendor/github.com/jinzhu/gorm:go_default_library",
        "//vendor/github.com/jinzhu/gorm/dialects/mysql:go_default_library",
        "//vendor/github.com/spf13/cobra:go_default_library",
    ],
)

filegroup(
    name = "configs",
    srcs = glob(["*.yaml"]),
)

filegroup(
    name = "package-srcs",
    srcs = glob(["**"]),
    tags = ["automanaged"],
    visibility = ["//visibility:private"],
)

filegroup(
    name = "all-srcs",
    srcs = [
        ":package-srcs",
        "//velodrome/transform/plugins:all-srcs",
    ],
    tags = ["automanaged"],
)
