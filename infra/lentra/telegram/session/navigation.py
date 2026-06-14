def push(stack, screen):
    stack.append(screen)
    return stack


def pop(stack):
    if len(stack) > 1:
        stack.pop()
    return stack


def current(stack):
    return stack[-1] if stack else None
