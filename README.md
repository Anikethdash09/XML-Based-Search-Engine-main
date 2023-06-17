# Building Efficient Search Engine for XML Files.
 
I have developed a search engine that uses the Wikipedia XML dataset to retrieve relevant results based on user queries. The engine is built using natural language processing techniques and information retrieval objectives. Users can input their search query and the engine parses through the entire XML file to display relevant results.

Changes:
- Caching added.
- MultiThreading Enabled.
- Improved Indexing Time.
- Developed Front End.
- Used BM-25 ranking over TF-IDF resulting better query output.
- Used joblib library instead of pickle resulting in less overheads and parralel processining resulting faster indexing.
- Separate Parameter to whether they want to have specific search_type in the output, resulting more flexibility to query results.


~ Developed by Abhisek Panda
