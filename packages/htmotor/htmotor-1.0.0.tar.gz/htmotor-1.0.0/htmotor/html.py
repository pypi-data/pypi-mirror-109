from dataclasses import dataclass


@dataclass
class HTML:
    """Base class for motor.

    Init:
        prevent_xss: bool = False
            For enable/disable html encoding.

    Public Functions:
        prevent_xss(text: str) -> str
        render(html: str, **kwargs) -> str
        render_file(path_like: str, **kwargs) -> str
    """

    # Constants
    VAR_REGEX: str = r"(\\?{%v +([a-zA-Z0-9]+) *%})"
    END_REGEX: str = r"(\\?{% *end *%})"
    FOR_REGEX: str = r"(\\?{%f +(.+ do) *%})"
    FOR_VAR_REGEX: str = r"(\\?{%fv +([a-zA-Z0-9]+) *%})"
    RESPONSIVE_REGEX: str = r"(\\?{% *responsive *%})"
    EVAL_REGEX: str = r"(\\?{%ev +(.+) *%})"
    EXEC_REGEX: str = r"(\\?{%ex +(.+) *%})"

    def __init__(self, prevent_xss: bool = False) -> None:
        self.xss = prevent_xss

        return None

    # Prevent XSS Function:
    def prevent_xss(self, text: str) -> str:
        """Encode HTML for prevent XSS.

        Parameters:
            text (str): The malicious text.

        Returns:
            str: Encoded string.
        """

        return "".join(
            f"&#{ord(i)};" for i in str(text)
        )

    # Render & Render File Functions:
    def render(self, htmotor: str, **kwargs) -> str:
        """Render htmotor syntax to HTML.

        Parameters:
            htmotor (str): Htmotor syntax.
            **kwargs (dict): Variables.

        Returns:
            str: Rendered HTML string.
        """

        minified = self.__minify(htmotor)
        variables = self.__render_variables(minified, kwargs)
        responsive = self.__render_responsive(variables)
        executed = self.__render_exec(responsive)
        evaled = self.__render_eval(executed)
        for_rendered = self.__render_for_loop(evaled, kwargs)
        return for_rendered

    def render_file(self, path_like: str, **kwargs) -> str:
        """Render htmotor syntax to HTML (from file.).

        Parameters:
            path_like (str): File path.
            **kwargs (dict): Variables.

        Returns:
            str: Rendered HTML string.
        """

        with open(path_like, "r", encoding="utf-8") as file:
            return self.render(file.read(), **kwargs)

    # Private Functions:
    def __minify(self, htmotor: str) -> str:
        return "\n".join(
            i.strip() for i in htmotor.splitlines()
        )

    def __render_variables(self, htmotor: str, kwargs: dict) -> str:
        from re import findall

        for result in findall(self.VAR_REGEX, htmotor):
            var = kwargs[result[1].strip()]
            should_encode = True

            if isinstance(var, tuple):
                should_encode = var[1]
                var = var[0]

            if self.xss and should_encode:
                var = self.prevent_xss(var)

            htmotor = htmotor.replace(
                result[0], var if not result[0].startswith("\\") else result[0][1:])

        return htmotor

    def __render_responsive(self, htmotor: str) -> str:
        from re import findall

        for result in findall(self.RESPONSIVE_REGEX, htmotor):
            htmotor = htmotor.replace(
                result, "<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")

        return htmotor

    def __render_exec(self, htmotor: str) -> str:
        from re import findall

        for result in findall(self.EXEC_REGEX, htmotor):
            match, code = result

            if match.startswith("\\"):
                htmotor = htmotor.replace(match, match[1:])
                continue

            result = exec(code, globals())
            htmotor = htmotor.replace(match, "")

        return htmotor

    def __render_eval(self, htmotor: str) -> str:
        from re import findall

        for result in findall(self.EVAL_REGEX, htmotor):
            match, code = result

            if match.startswith("\\"):
                htmotor = htmotor.replace(match, match[1:])
                continue

            result = eval(code)
            htmotor = htmotor.replace(match, self.prevent_xss(result))

        return htmotor

    def __render_for_loop(self, htmotor: str, kwargs: dict) -> str:
        from re import findall
        index = 0

        for result in findall(self.FOR_REGEX, htmotor):
            full, loop = result

            if full.startswith("\\"):
                htmotor = htmotor.replace(full, full[1:])
                continue

            index = htmotor.find(full, index)

            content = ""
            full_text = full

            for line in htmotor[index + len(full):].splitlines():
                full_text += line + "\n"
                if findall(self.FOR_REGEX, line):
                    raise SyntaxError(
                        "You can't use for loop inside a for loop.")
                elif findall(self.END_REGEX, line):
                    full_text = full_text[:-1]
                    break
                else:
                    content += line

            content = self.__render_for_loop(content, kwargs)

            for for_variable in findall(self.FOR_VAR_REGEX, content):
                content = content.replace(for_variable[0], "{{{0}}}".format(
                    for_variable[1] if not self.xss else "encode_string({0})".format(
                        for_variable[1])
                ))

            exec_local = {
                "encode_string": self.prevent_xss,
                **kwargs
            }

            evaled_text = "def temp_for_func():\n array = []\n for {0}:\n  array.append(f'{1}')\n\n return array".format(
                loop.strip().rstrip("do"),
                content.replace("\"", "\\\"").replace("'", "\\'")
            )

            exec(evaled_text, exec_local)
            result = exec_local["temp_for_func"]()

            htmotor = htmotor.replace(full_text, "".join(result))

        return htmotor
