package perftest

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class PerformanceTest extends Simulation {

  val httpProtocol = http
    .baseUrl("http://localhost:8000")
    
  val request_body = StringBody("""{ "url": "https://www.reddit.com/" }""")
  val content_headers = Map("Content-Type" -> "application/json")
  
  val writeChain = exec(http("post url")
    .post("/shorten_url")
    .headers(content_headers)
    .body(request_body)
    .check(jsonPath("$.shortened_url").saveAs("shortened_url"))
    .check(status.is(201))
  )
  
  val readChain = exec(http("get by url")
    .get("${shortened_url}")
    .disableFollowRedirect
    .check(status.is(301))
  )
  
  val mainChain = writeChain
        .repeat(9)
        {
            readChain            
        }

  val fullScenario = scenario("Shorten Url") 
    .exec(mainChain)
  
  setUp(fullScenario.inject(atOnceUsers(500)).protocols(httpProtocol))
}
