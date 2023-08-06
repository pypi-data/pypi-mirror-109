"""
Forum related views
"""

import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from aa_forum.constants import SETTING_MESSAGESPERPAGE, SETTING_TOPICSPERPAGE
from aa_forum.forms import NewTopicForm, ReplyForm
from aa_forum.models import Boards, Categories, Messages, Settings, Topics


@login_required
@permission_required("aa_forum.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Forum index view
    :param request:
    :type request:
    :return:
    :rtype:
    """

    categories = (
        Categories.objects.prefetch_related(
            Prefetch(
                "boards",
                queryset=Boards.objects.prefetch_related("messages")
                .filter(
                    Q(groups__in=request.user.groups.all()) | Q(groups__isnull=True),
                    parent_board__isnull=True,
                )
                .distinct()
                .annotate(
                    num_posts=Count("messages", distinct=True),
                    num_topics=Count("topics", distinct=True),
                )
                .order_by("order"),
            )
        )
        .all()
        .order_by("order")
    )

    context = {"categories": categories}

    return render(request, "aa_forum/view/forum/index.html", context)


@login_required
@permission_required("aa_forum.basic_access")
def board(
    request: WSGIRequest, category_slug: str, board_slug: str, page_number: int = None
) -> HttpResponse:
    """
    Forum board view
    :param request:
    :type request:
    :param category_slug:
    :type category_slug:
    :param board_slug:
    :type board_slug:
    :return:
    :rtype:
    """

    try:
        board = (
            Boards.objects.prefetch_related("messages")
            # .prefetch_related("child_boards")
            .prefetch_related(
                Prefetch(
                    "topics",
                    queryset=Topics.objects.prefetch_related("messages")
                    .distinct()
                    .annotate(
                        num_posts=Count("messages", distinct=True),
                    )
                    .order_by("-is_sticky", "-time_modified"),
                )
            )
            .filter(
                Q(groups__in=request.user.groups.all()) | Q(groups__isnull=True),
                category__slug__slug__exact=category_slug,
                slug__slug__exact=board_slug,
            )
            .distinct()
            .get()
        )
    except Boards.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4><p>The board you were trying to visit does "
                    "either not exist, or you don't have access to it ...</p> "
                )
            ),
        )

        return redirect("aa_forum:forum_index")

    paginator = Paginator(
        board.topics.all(),
        int(Settings.objects.get_setting(setting_key=SETTING_TOPICSPERPAGE)),
    )
    page_obj = paginator.get_page(page_number)

    context = {"board": board, "page_obj": page_obj}

    return render(request, "aa_forum/view/forum/board.html", context)


@login_required
@permission_required("aa_forum.basic_access")
def board_new_topic(
    request: WSGIRequest, category_slug: str, board_slug: str
) -> HttpResponse:
    """
    Beginn a new topic
    :param request:
    :type request:
    :param category_slug:
    :type category_slug:
    :param board_slug:
    :type board_slug:
    :return:
    :rtype:
    """

    try:
        Categories.objects.get(slug__slug__exact=category_slug)
    except Categories.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4><p>The category you were trying to post in does "
                    "not exist ...</p> "
                )
            ),
        )

        return redirect("aa_forum:forum_index")

    try:
        board = (
            Boards.objects.filter(
                Q(groups__in=request.user.groups.all()) | Q(groups__isnull=True),
                category__slug__slug__exact=category_slug,
                slug__slug__exact=board_slug,
            )
            .distinct()
            .get()
        )
    except Boards.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4><p>The board you were trying to post in does "
                    "either not exist, or you don't have access to it ...</p> "
                )
            ),
        )

        return redirect("aa_forum:forum_index")

    # If this is a POST request we need to process the form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = NewTopicForm(request.POST)

        # Check whether it's valid:
        if form.is_valid():
            user_started = request.user
            user_updated = request.user
            post_time = timezone.now()

            topic = Topics()
            topic.board = board
            topic.user_started = user_started
            topic.user_updated = user_updated
            topic.time_modified = post_time
            topic.subject = form.cleaned_data["subject"]
            topic.save()

            message = Messages()
            message.topic = topic
            message.board = board
            message.user_created = user_started
            message.message = form.cleaned_data["message"]
            message.save()

            # Set topic and message as "read by" by the author
            topic.read_by.add(user_updated)
            message.read_by.add(request.user)

            return redirect(
                "aa_forum:forum_board",
                category_slug=board.category.slug.slug,
                board_slug=board.slug.slug,
            )

    # If not, we'll create a blank form
    else:
        form = NewTopicForm()

    context = {"board": board, "form": form}

    return render(request, "aa_forum/view/forum/new-topic.html", context)


@login_required
@permission_required("aa_forum.basic_access")
def topic(
    request: WSGIRequest,
    category_slug: str,
    board_slug: str,
    topic_slug: str,
    page_number: int = None,
) -> HttpResponse:
    """
    View a topic
    :param request:
    :type request:
    :param category_slug:
    :type category_slug:
    :param board_slug:
    :type board_slug:
    :param topic_slug:
    :type topic_slug:
    :param page_number:
    :type page_number:
    :return:
    :rtype:
    """

    try:
        Boards.objects.prefetch_related("messages").filter(
            Q(groups__in=request.user.groups.all()) | Q(groups__isnull=True),
            category__slug__slug__exact=category_slug,
            slug__slug__exact=board_slug,
        ).distinct().get()
    except Boards.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4><p>The topic you were trying to view does "
                    "either not exist, or you don't have access to it ...</p> "
                )
            ),
        )

        return redirect("aa_forum:forum_index")

    topic = Topics.objects.get(slug__slug__exact=topic_slug)
    topic_messages = Messages.objects.filter(topic=topic)

    # Set this topic as "read by" by the current user
    topic.read_by.add(request.user)

    paginator = Paginator(
        topic_messages,
        int(Settings.objects.get_setting(setting_key=SETTING_MESSAGESPERPAGE)),
    )
    page_obj = paginator.get_page(page_number)

    reply_form = ReplyForm()

    context = {"topic": topic, "page_obj": page_obj, "reply_form": reply_form}

    return render(request, "aa_forum/view/forum/topic.html", context)


@login_required
@permission_required("aa_forum.basic_access")
def topic_reply(
    request: WSGIRequest, category_slug: str, board_slug: str, topic_slug: str
) -> HttpResponse:
    """
    Reply to posts in a topic
    :param request:
    :type request:
    :param category_slug:
    :type category_slug:
    :param board_slug:
    :type board_slug:
    :param topic_slug:
    :type topic_slug:
    :return:
    :rtype:
    """

    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = ReplyForm(request.POST)

        # Check whether it's valid:
        if form.is_valid():
            board = Boards.objects.get(slug__slug__exact=board_slug)
            topic = Topics.objects.get(slug__slug__exact=topic_slug)

            new_message = Messages()
            new_message.topic = topic
            new_message.board = board
            new_message.user_created = request.user
            new_message.message = form.cleaned_data["message"]
            new_message.save()

            # Update the modified timestamp on the topic
            topic.time_modified = timezone.now()
            topic.save()

            # Remove all users from "read by" list and set the current user again.
            # This way we mark this topic as unread for all but the current user.
            topic.read_by.clear()
            topic.read_by.add(request.user)

            # Set the message as "read by" the author
            new_message.read_by.add(request.user)

            return redirect(
                "aa_forum:forum_message_entry_point_in_topic", new_message.id
            )

    messages.warning(
        request,
        mark_safe(_("<h4>Warning!</h4><p>Something went wrong, please try again</p>.")),
    )

    return redirect("aa_forum:forum_topic", category_slug, board_slug, topic_slug)


@login_required
@permission_required("aa_forum.manage_forum")
def topic_change_lock_state(
    request: WSGIRequest, topic_id: int
) -> HttpResponseRedirect:
    """
    Change the lock state of the given topic
    :param request:
    :type request:
    :param topic_id:
    :type topic_id:
    :return:
    :rtype:
    """

    topic = Topics.objects.get(pk=topic_id)

    if topic.is_locked:
        topic.is_locked = False

        messages.success(
            request,
            mark_safe(_("<h4>Success!</h4><p>Topic has been unlocked/re-opened.</p>")),
        )
    else:
        topic.is_locked = True

        messages.success(
            request,
            mark_safe(_("<h4>Success!</h4><p>Topic has been locked/closed.</p>")),
        )

    topic.save()

    return redirect("aa_forum:forum_board", topic.board.category.slug, topic.board.slug)


@login_required
@permission_required("aa_forum.manage_forum")
def topic_change_sticky_state(
    request: WSGIRequest, topic_id: int
) -> HttpResponseRedirect:
    """
    Change the sticky state of the given topic
    :param request:
    :type request:
    :param topic_id:
    :type topic_id:
    :return:
    :rtype:
    """

    topic = Topics.objects.get(pk=topic_id)

    if topic.is_sticky:
        topic.is_sticky = False

        messages.success(
            request,
            mark_safe(_('<h4>Success!</h4><p>Topic is no longer "Sticky".</p>')),
        )
    else:
        topic.is_sticky = True

        messages.success(
            request,
            mark_safe(_('<h4>Success!</h4><p>Topic is now "Sticky".</p>')),
        )

    topic.save()

    return redirect("aa_forum:forum_board", topic.board.category.slug, topic.board.slug)


@login_required
@permission_required("aa_forum.manage_forum")
def topic_delete(request: WSGIRequest, topic_id: int) -> HttpResponseRedirect:
    """
    Delete a given topic
    :param request:
    :type request:
    :param topic_id:
    :type topic_id:
    """

    topic = Topics.objects.get(pk=topic_id)
    board = topic.board

    topic.delete()

    messages.success(
        request,
        mark_safe(_("<h4>Success!</h4><p>Topic removed.</p>")),
    )

    return redirect("aa_forum:forum_board", board.category.slug, board.slug)


@login_required
@permission_required("aa_forum.basic_access")
def message_entry_point_in_topic(
    request: WSGIRequest, message_id: int
) -> HttpResponseRedirect:
    """
    Get a messages antry point in a topic, so we end up on the right page with it
    :param request:
    :type request:
    :param message_id:
    :type message_id:
    """

    try:
        message = Messages.objects.get(pk=message_id)
    except Messages.DoesNotExist:
        messages.error(
            request,
            mark_safe(_("<h4>Error!</h4><p>The message doesn't exist ...</p> ")),
        )

        return redirect("aa_forum:forum_index")

    try:
        board = (
            Boards.objects.filter(
                Q(groups__in=request.user.groups.all()) | Q(groups__isnull=True),
                pk=message.board.pk,
            )
            .distinct()
            .get()
        )
    except Boards.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4><p>The topic you were trying to view does "
                    "either not exist, or you don't have access to it ...</p> "
                )
            ),
        )

        return redirect("aa_forum:forum_index")

    messages_in_topic = Messages.objects.filter(pk__lte=message.pk, topic=message.topic)
    number_of_messages_in_topic = messages_in_topic.count()
    settings = Settings.objects.all()
    messages_per_topic = settings.values_list("value", flat=True).get(
        variable__exact="defaultMaxMessages"
    )

    page = int(math.ceil(int(number_of_messages_in_topic) / int(messages_per_topic)))

    if page > 1:
        redirect_path = reverse(
            "aa_forum:forum_topic",
            args=(
                board.category.slug,
                board.slug,
                message.topic.slug,
                page,
            ),
        )
        redirect_url = f"{redirect_path}#message-{message.pk}"
    else:
        redirect_path = reverse(
            "aa_forum:forum_topic",
            args=(board.category.slug, board.slug, message.topic.slug),
        )
        redirect_url = f"{redirect_path}#message-{message.pk}"

    return HttpResponseRedirect(redirect_url)
