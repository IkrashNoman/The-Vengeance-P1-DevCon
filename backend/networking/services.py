"""
Networking Service Module
Handles semantic matching for attendee networking using AI
Matches attendees based on interests, expertise, and goals
"""

import logging
from typing import List, Dict, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Semantic matching imports
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    SEMANTIC_MATCHING_AVAILABLE = True
except ImportError:
    SEMANTIC_MATCHING_AVAILABLE = False
    logger.warning("Semantic matching dependencies not installed. Matching service will be limited.")

from .models import NetworkProfile, RecommendedConnection
from accounts.models import User
from django.db.models import Q


class NetworkMatchingService:
    """
    AI-powered networking matching service
    Uses semantic similarity to recommend connections between attendees
    """
    
    def __init__(self):
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize transformer model for semantic matching"""
        if not SEMANTIC_MATCHING_AVAILABLE:
            logger.warning("Semantic matching not available")
            return False
        
        try:
            # Use lighter model for faster processing
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Semantic matching model initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize matching service: {str(e)}")
            return False
    
    def create_semantic_profile(self, network_profile: NetworkProfile) -> str:
        """
        Create semantic profile string from network profile
        
        Args:
            network_profile: NetworkProfile instance
        
        Returns:
            Semantic profile string for embedding
        """
        dept = network_profile.user.username or "General"
        interests = ", ".join(network_profile.interests) if network_profile.interests else "General"
        expertise = ", ".join(network_profile.expertise) if network_profile.expertise else "General"
        job_title = network_profile.job_title or "Professional"
        
        return (
            f"Department: {dept} | "
            f"Job Title: {job_title} | "
            f"Interests: {interests} | "
            f"Expertise: {expertise}"
        )
    
    def find_top_matches(
        self, 
        target_profile: NetworkProfile, 
        top_n: int = 3,
        min_score: float = 0.4
    ) -> List[Dict]:
        """
        Find top semantic matches for a profile
        
        Args:
            target_profile: Target NetworkProfile to find matches for
            top_n: Number of top matches to return
            min_score: Minimum similarity score threshold
        
        Returns:
            List of match dictionaries with user info and scores
        """
        if not SEMANTIC_MATCHING_AVAILABLE or not self.model:
            logger.error("Semantic matching not available")
            return []
        
        try:
            # Get other discoverable profiles
            other_profiles = NetworkProfile.objects.filter(
                show_in_discovery=True,
                user__tenant=target_profile.user.tenant
            ).exclude(user=target_profile.user)
            
            if not other_profiles.exists():
                logger.info("No other discoverable profiles found")
                return []
            
            # Create semantic profiles
            target_semantic = self.create_semantic_profile(target_profile)
            other_semantics = [
                self.create_semantic_profile(profile) 
                for profile in other_profiles
            ]
            
            # Get embeddings
            target_embedding = self.model.encode(target_semantic)
            other_embeddings = self.model.encode(other_semantics)
            
            # Calculate similarities
            similarities = cosine_similarity(
                [target_embedding], 
                other_embeddings
            ).flatten()
            
            # Get indices of top matches
            best_indices = np.argsort(similarities)[-top_n:][::-1]
            
            # Build match results
            matches = []
            for rank, idx in enumerate(best_indices, 1):
                similarity_score = float(similarities[idx])
                
                if similarity_score < min_score:
                    continue
                
                matched_profile = list(other_profiles)[idx]
                reason = self._determine_match_reason(target_profile, matched_profile)
                
                matches.append({
                    'rank': rank,
                    'user_id': matched_profile.user.id,
                    'name': matched_profile.user.get_full_name() or matched_profile.user.email,
                    'email': matched_profile.user.email,
                    'job_title': matched_profile.job_title,
                    'company': matched_profile.company,
                    'interests': matched_profile.interests,
                    'expertise': matched_profile.expertise,
                    'match_score': similarity_score,
                    'reason': reason
                })
            
            logger.info(f"Found {len(matches)} matches for {target_profile.user.email}")
            return matches
            
        except Exception as e:
            logger.error(f"Error finding matches: {str(e)}")
            return []
    
    def _determine_match_reason(
        self, 
        profile1: NetworkProfile, 
        profile2: NetworkProfile
    ) -> str:
        """
        Determine reason for recommendation
        
        Args:
            profile1: First profile
            profile2: Second profile
        
        Returns:
            String describing match reason
        """
        common_interests = set(profile1.interests or []) & set(profile2.interests or [])
        common_expertise = set(profile1.expertise or []) & set(profile2.expertise or [])
        
        reasons = []
        
        if common_interests:
            reasons.append(f"Common interests in {', '.join(list(common_interests)[:2])}")
        
        if common_expertise:
            reasons.append(f"Aligned expertise in {', '.join(list(common_expertise)[:2])}")
        
        if profile1.user.username == profile2.user.username:
            reasons.append("Same department")
        
        if not reasons:
            reasons.append("Aligned professional profiles")
        
        return " | ".join(reasons)
    
    def batch_recommend_matches(
        self, 
        tenant_id: int,
        batch_size: int = 10
    ) -> Dict[int, List[Dict]]:
        """
        Generate recommendations for all users in a tenant
        
        Args:
            tenant_id: Tenant ID to generate recommendations for
            batch_size: Number of profiles to process in each batch
        
        Returns:
            Dictionary mapping user_id to list of recommendations
        """
        if not SEMANTIC_MATCHING_AVAILABLE:
            return {}
        
        try:
            # Get all profiles for tenant
            profiles = NetworkProfile.objects.filter(
                show_in_discovery=True,
                user__tenant_id=tenant_id
            )
            
            recommendations = {}
            
            for profile in profiles[:batch_size]:
                matches = self.find_top_matches(profile, top_n=5)
                if matches:
                    recommendations[profile.user.id] = matches
            
            logger.info(f"Generated recommendations for {len(recommendations)} users")
            return recommendations
            
        except Exception as e:
            logger.error(f"Batch recommendation error: {str(e)}")
            return {}
    
    def calculate_network_graph(self, tenant_id: int) -> Dict:
        """
        Calculate network graph data for visualization
        
        Args:
            tenant_id: Tenant ID to calculate graph for
        
        Returns:
            Dictionary with nodes and edges for visualization
        """
        if not SEMANTIC_MATCHING_AVAILABLE or not self.model:
            return {'nodes': [], 'edges': []}
        
        try:
            # Get all discoverable profiles
            profiles = NetworkProfile.objects.filter(
                show_in_discovery=True,
                user__tenant_id=tenant_id
            )
            
            if not profiles.exists():
                return {'nodes': [], 'edges': []}
            
            # Create nodes
            nodes = []
            for profile in profiles:
                nodes.append({
                    'id': profile.user.id,
                    'label': profile.user.get_full_name() or profile.user.email,
                    'department': profile.user.username or 'General',
                    'title': profile.job_title or 'Professional',
                    'image': str(profile.user.profile_picture.url) if hasattr(profile.user, 'profile_picture') else None
                })
            
            # Calculate edges (top 2 matches per person)
            edges = []
            profile_list = list(profiles)
            
            if len(profile_list) > 1:
                # Create semantic embeddings for all profiles
                semantics = [self.create_semantic_profile(p) for p in profile_list]
                embeddings = self.model.encode(semantics)
                sim_matrix = cosine_similarity(embeddings)
                
                # For each user, find top 2 matches
                for i, profile in enumerate(profile_list):
                    similarities = sim_matrix[i]
                    # Exclude self (similarity = 1.0)
                    best_indices = np.argsort(similarities)[:-1][-2:][::-1]
                    
                    for match_idx in best_indices:
                        score = float(similarities[match_idx])
                        if score > 0.3:  # Minimum threshold
                            edges.append({
                                'source': profile.user.id,
                                'target': profile_list[match_idx].user.id,
                                'weight': score,
                                'label': f"{int(score * 100)}% Match"
                            })
            
            return {
                'nodes': nodes,
                'edges': edges
            }
            
        except Exception as e:
            logger.error(f"Network graph calculation error: {str(e)}")
            return {'nodes': [], 'edges': []}


class ConnectionRecommendationService:
    """
    Service for managing connection recommendations
    """
    
    @staticmethod
    def create_recommendation(
        user: User,
        recommended_user: User,
        match_score: float,
        reason: str
    ) -> RecommendedConnection:
        """
        Create or update a recommendation
        
        Args:
            user: Target user
            recommended_user: Recommended user to connect with
            match_score: Similarity score (0.0-1.0)
            reason: Reason for recommendation
        
        Returns:
            RecommendedConnection instance
        """
        rec, created = RecommendedConnection.objects.update_or_create(
            user=user,
            recommended_user=recommended_user,
            defaults={
                'match_score': match_score,
                'reason': reason
            }
        )
        return rec
    
    @staticmethod
    def get_recommendations_for_user(user: User, limit: int = 5) -> List[RecommendedConnection]:
        """
        Get recommendations for a user
        
        Args:
            user: Target user
            limit: Maximum number of recommendations to return
        
        Returns:
            QuerySet of recommendations ordered by match score
        """
        return RecommendedConnection.objects.filter(
            user=user
        ).order_by('-match_score')[:limit]
    
    @staticmethod
    def accept_recommendation(
        recommendation: RecommendedConnection,
        message: str = ""
    ):
        """
        Accept a recommendation and create connection request
        
        Args:
            recommendation: RecommendedConnection to accept
            message: Optional message for connection request
        
        Returns:
            Created Connection object
        """
        from .models import Connection
        
        connection, created = Connection.objects.get_or_create(
            user_from=recommendation.user,
            user_to=recommendation.recommended_user,
            defaults={
                'status': 'pending',
                'message': message
            }
        )
        
        # Mark recommendation as converted
        recommendation.was_connected = True
        recommendation.save()
        
        return connection


# Global service instance
_matching_service_instance = None


def get_matching_service() -> NetworkMatchingService:
    """
    Get or create global matching service instance
    
    Returns:
        NetworkMatchingService instance
    """
    global _matching_service_instance
    if _matching_service_instance is None:
        _matching_service_instance = NetworkMatchingService()
    return _matching_service_instance
