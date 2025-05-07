# Using the Extracted YouTube URLs with n8n

After extracting your YouTube URLs to a CSV file, you can use n8n to process them and recreate your playlists. This guide provides instructions for setting up an n8n workflow to process your large dataset of YouTube links.

## Setting Up n8n

1. Install n8n by following the [official installation guide](https://docs.n8n.io/hosting/)
2. Create a new workflow in n8n

## n8n Workflow for Processing Large CSV Files

### Step 1: Read and Parse CSV

```
[Read Binary File] → [CSV Parse]
```

1. **Read Binary File Node**:
   - Set the "File Path" to your extracted YouTube links CSV
   - Keep "Property Name" as `data`

2. **CSV Parse Node**:
   - Set "CSV Input Data" to `data` from previous node
   - Enable "Parse as String" for the URL column

### Step 2: Process in Batches to Handle Large Datasets

```
[CSV Parse] → [Split in Batches]
```

1. **Split in Batches Node**:
   - Set "Batch Size" to 50
   - This prevents memory issues with large datasets

### Step 3: Get Video Information

```
[Split in Batches] → [Code] → [HTTP Request]
```

1. **Code Node** (to prepare URLs for HTTP requests):
   ```javascript
   // Process each item in the batch
   return items.map(item => {
     // Extract video ID from URL
     let videoId = null;
     
     if (item.json.url.includes('youtube.com/watch?v=')) {
       videoId = item.json.url.split('v=')[1].split('&')[0];
     } else if (item.json.url.includes('youtu.be/')) {
       videoId = item.json.url.split('youtu.be/')[1].split('?')[0];
     }
     
     return {
       json: {
         ...item.json,
         videoId,
         apiUrl: videoId ? `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=snippet,contentDetails&key=YOUR_API_KEY` : null
       }
     };
   });
   ```

2. **HTTP Request Node**:
   - Set "Request Method" to GET
   - Set "URL" to `={{$json.apiUrl}}`
   - Use "Continue on Fail" to handle any errors

### Step 4: Extract and Categorize Video Information

```
[HTTP Request] → [Code] → [Set]
```

1. **Code Node** (to parse response and categorize):
   ```javascript
   // Process HTTP responses
   return items.map(item => {
     try {
       // Skip items that failed or have no response
       if (!item.json || !item.json.body || item.json.body.items.length === 0) {
         return {
           json: {
             ...item.json,
             status: 'error',
             title: null,
             description: null,
             category: null
           }
         };
       }
       
       const videoData = item.json.body.items[0];
       const title = videoData.snippet.title;
       const description = videoData.snippet.description;
       const tags = videoData.snippet.tags || [];
       
       // Basic categorization logic - can be enhanced with AI
       let category = 'Uncategorized';
       
       // Simple keyword-based categorization
       const lowerTitle = title.toLowerCase();
       const lowerDesc = description.toLowerCase();
       const lowerTags = tags.join(' ').toLowerCase();
       
       if (lowerTitle.includes('music') || lowerDesc.includes('song') || lowerTags.includes('music')) {
         category = 'Music';
       } else if (lowerTitle.includes('tutorial') || lowerDesc.includes('learn') || lowerTags.includes('education')) {
         category = 'Education';
       } else if (lowerTitle.includes('game') || lowerDesc.includes('gaming') || lowerTags.includes('gameplay')) {
         category = 'Gaming';
       }
       // Add more categories as needed
       
       return {
         json: {
           ...item.json,
           status: 'success',
           title,
           description,
           category
         }
       };
     } catch (error) {
       return {
         json: {
           ...item.json,
           status: 'error',
           error: error.message
         }
       };
     }
   });
   ```

### Step 5: Group by Category

```
[Set] → [Split Into Groups]
```

1. **Split Into Groups Node**:
   - Set "Group Output By" to `category`

### Step 6: Create Playlists and Add Videos

```
[Split Into Groups] → [YouTube]
```

1. **YouTube Node** (to create playlists):
   - Set "Operation" to "Create"
   - Set "Resource" to "Playlist"
   - Set "Title" to `={{$node["SplitIntoGroups"].context["groupName"]}} Playlist`
   - Connect to another YouTube node

2. **YouTube Node** (to add videos to playlist):
   - Set "Operation" to "Add"
   - Set "Resource" to "Playlist Item"
   - Set "Playlist ID" to `={{$json.playlistId}}`
   - Set "Video ID" to `={{$json.videoId}}`

## Advanced: Using AI for Better Categorization

You can enhance the categorization by adding an AI node before the grouping:

```
[HTTP Request] → [Code] → [OpenAI] → [Set]
```

The OpenAI node would analyze the video title and description to provide more accurate categorization.

## Handling Rate Limits

YouTube API has rate limits. To work around them:

1. Add a **Wait** node between API requests (set to 1-2 seconds)
2. Add error handling with retries for failed requests
3. Consider splitting your workflow across multiple days for large datasets

## Final Tips

1. Start with a small subset of your data to test the workflow
2. Save intermediate results to avoid reprocessing if errors occur
3. Consider using a caching mechanism for API responses to avoid redundant calls

Remember to replace `YOUR_API_KEY` with an actual YouTube API key in the workflow.