from core.utils import rank_hot, rank_top

# Comments
def get_comment_list(comments=None, rankby="hot"):
    """Recursively build a list of comments."""

    # Loop through all the comments I've passed
    for comment in comments:
        # yield 'in' to open a comment container. Always before the comment.
        yield 'in'
        # Add comment to the list
        yield comment
        # get comment's children
        children = comment.children.all()
        if children:
            # Rank children
            ranked_children = children.order_by('score', '-created_at')
            # loop through children, and apply this function
            for x in get_comment_list(ranked_children, rankby=rankby):
                # yield children to insert all of them into the comment.
                yield x
        # yield 'out' at the end of the comment, after you have inserted all of the children
        yield 'out'

