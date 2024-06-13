<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
</head>
<body>
    <div class="ui container" style="padding-top: 10px;">
        <h1 class="ui header">News Recommendations</h1>
        <table class="ui celled table">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>#Likes</th>
                    <th>#Comments</th>
                </tr>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}" target="_blank">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="4">
                        <a href="/update" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                        <a href="/recommendations" class="ui right floated small secondary button">Show Recommendations</a>
                    </th>
                </tr>
            </tfoot>
        </table>
    </div>
</body>
</html>
