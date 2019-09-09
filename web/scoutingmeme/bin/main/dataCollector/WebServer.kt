package dataCollector

import java.net.ServerSocket
import java.net.Socket

/**
 * WebServer Object.
 *
 * WebServer represents a server that serves up web content through its
 * ServerSocket. Listens indefinitely for new client connections and creates
 * a new thread to handle client requests.
 *
 * @author Maurice Harris 1000882916
 */
object WebServer {

    /**
     * Creates the ServerSocket and listens for client connections, creates a
     * separate thread to handle each client request.
     *
     * @param args an array of arguments to be used in the
     */
    @Throws(Exception::class)
    @JvmStatic
    fun main(args: Array<String>) {

        // Create ServerSocket on LocalHost, port 6789
        val serverSocket = ServerSocket(6789)
        println("Listening for connections on port 6789...\r\n")

        // Listen for new client connections
        while (true) {

            // Accept new client connection
            val connectionSocket = serverSocket.accept()

            // Create new thread to handle client request
            val connectionThread = Thread(Connection(connectionSocket))

            // Start the connection thread
            connectionThread.start()
            println("New connection on port 6789...\r\n")
        }
    }
}
