def test_analytics_admin_list_display(admin_instance):
    assert admin_instance.list_display == (
        "page",
        "method",
        "date",
        "view_count",
        "username",
        "exists",
        "origin",
        "user_agent",
    )


def test_analytics_admin_list_filter(admin_instance):
    assert admin_instance.list_filter == (
        "exists",
        "date",
        "method",
        "origin",
        "username",
        "page",
    )
