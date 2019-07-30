package uk.vh7.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import uk.vh7.model.ShortLink;

@Repository
public interface ShortLinkRepository extends JpaRepository<ShortLink, Long> {

}
