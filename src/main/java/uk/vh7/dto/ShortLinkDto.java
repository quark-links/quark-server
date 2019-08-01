package uk.vh7.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.stereotype.Component;

import java.util.Date;

@Component
public class ShortLinkDto {
    @JsonIgnore
    private Long id;

    private String longUrl;

    @JsonIgnore
    private Date createdAt;

    @JsonIgnore
    private Date updatedAt;

    @JsonIgnore
    private String shortLink;

    @JsonIgnore
    public void setId(Long id) {
        this.id = id;
    }

    @JsonProperty("id")
    public Long getId() {
        return id;
    }

    public void setLongUrl(String longUrl) {
        this.longUrl = longUrl;
    }

    public String getLongUrl() {
        return longUrl;
    }

    @JsonIgnore
    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    @JsonProperty("createdAt")
    public Date getCreatedAt() {
        return createdAt;
    }

    @JsonIgnore
    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    @JsonProperty("updatedAt")
    public Date getUpdatedAt() {
        return updatedAt;
    }

    @JsonIgnore
    public void setShortLink(String shortLink) {
        this.shortLink = shortLink;
    }

    @JsonProperty("shortLink")
    public String getShortLink() {
        return shortLink;
    }
}
