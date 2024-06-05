<!DOCTYPE html>
<html>
<head>
    <title>Recommendations</title>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
</head>
<body>
    <div class="ui container" style="padding-top: 10px;">
    <h1>Recommended News</h1>
    <table class="ui celled table">
        <thead>
            <th>Title</th>
            <th>Author</th>
            <th>URL</th>
            <th>Comments</th>
            <th>Points</th>
            <th>Label</th>
        </thead>
        <tbody>
            % for row in rows:
            <tr>
                <td><a href="{{ row['url'] }}">{{ row['title'] }}</a></td>
                <td>{{ row['author'] }}</td>
                <td>{{ row['comments'] }}</td>
                <td>{{ row['points'] }}</td>
                <td>{{ row['label'] }}</td>
            </tr>
            % end
        </tbody>
    </table>
    <a href="/news" class="ui button">Back to News</a>
    </div>
</body>
</html>
