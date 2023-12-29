from qaSystem.question_answering_logical import loop_main


def main():
    while True:
        qa = loop_main()
        if qa == 1:
            return 0


if __name__ == '__main__':
    main()
