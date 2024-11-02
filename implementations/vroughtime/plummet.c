#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <assert.h>
#include <inttypes.h>

#include "vrt.h"

#define PORT 2002
#define HOST "roughtime-server"
#define RECV_BUFFER_LEN 1024

// Ixu7gqjJ9TU6IxsO8wxZxAFT5te6FcZZQq5vXFl35JE= | base64 -D | xxd -i
static uint8_t public_key_plummet[] = {
  0x23, 0x1b, 0xbb, 0x82, 0xa8, 0xc9, 0xf5, 0x35, 0x3a, 0x23, 0x1b, 0x0e,
  0xf3, 0x0c, 0x59, 0xc4, 0x01, 0x53, 0xe6, 0xd7, 0xba, 0x15, 0xc6, 0x59,
  0x42, 0xae, 0x6f, 0x5c, 0x59, 0x77, 0xe4, 0x91};

#define CHECK(x)                                                               \
  do {                                                                         \
    int ret;                                                                   \
    if ((ret = x) != VRT_SUCCESS) {                                            \
      return (ret);                                                            \
    }                                                                          \
  } while (0)

int prepare_socket(void)
{
  int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

  assert(sockfd >= 0);
  return sockfd;
}

void prepare_servaddr(struct sockaddr_in *servaddr)
{
  struct hostent *he;
  he = gethostbyname(HOST);
  assert(he != NULL);

  bzero((char *)servaddr, sizeof(*servaddr));

  char **ip_addr;
  memcpy(&ip_addr, &(he->h_addr_list[0]), sizeof(void *));
  memcpy(&servaddr->sin_addr.s_addr, ip_addr, sizeof(struct in_addr));

  servaddr->sin_family = AF_INET;
  servaddr->sin_port = htons(PORT);
}

int main(int argc, char **argv) {
  uint32_t recv_buffer[RECV_BUFFER_LEN / 4] = {0};
  uint8_t query[VRT_QUERY_PACKET_LEN] = {0};
  struct sockaddr_in servaddr;
  
  int sockfd = prepare_socket();
  prepare_servaddr(&servaddr);

  /* prepare query */
  uint8_t nonce[VRT_NONCE_SIZE] = "are you supposed to be looking here";
  CHECK(vrt_make_query(nonce, 64, query, sizeof query));

  /* send query */
  int n = sendto(sockfd, (const char *)query, sizeof query, 0,
             (const struct sockaddr *)&servaddr, sizeof(servaddr));

  /* receive packet */
  assert(n==sizeof query);
  do {
    n = recv(sockfd, recv_buffer, (sizeof recv_buffer) * sizeof recv_buffer[0], 0 /* flags */);
  } while (n == -1 && errno == EINTR);

  /* parse response */
  uint64_t out_midpoint;
  uint32_t out_radii;

  CHECK(vrt_parse_response(nonce, 64, recv_buffer,
                            sizeof recv_buffer * sizeof recv_buffer[0],
                            public_key_plummet, &out_midpoint,
                            &out_radii));
  printf("midp %" PRIu64 " radi %u\n", out_midpoint, out_radii);
  close(sockfd);

  (void)public_key_plummet;

  return 0;
}
